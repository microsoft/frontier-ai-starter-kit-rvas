"""Offline regression checks; no Azure credentials or SDK packages are needed."""
from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

import _shared
import compare_models
import grounded_answer
import probe_permissions
import probe_surface


class EnvironmentTests(unittest.TestCase):
    def test_process_overrides_required_and_optional_file_values(self):
        with tempfile.TemporaryDirectory() as directory:
            env_file = Path(directory) / ".env"
            env_file.write_text("REQUIRED=file\nOPTIONAL=file\nEMPTY=file\n", encoding="utf-8")
            with patch.object(_shared, "ENV_FILE", env_file), patch.dict(
                os.environ, {"REQUIRED": "process", "OPTIONAL": "process", "EMPTY": ""}, clear=True
            ):
                self.assertEqual(
                    _shared.load_env(("REQUIRED",)),
                    {"REQUIRED": "process", "OPTIONAL": "process", "EMPTY": ""},
                )

    def test_deploy_stops_before_mutation_without_a_user(self):
        with tempfile.TemporaryDirectory() as directory:
            az = Path(directory) / "az"
            log = Path(directory) / "calls"
            az.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$AZ_TEST_LOG"\nexit 1\n',
                encoding="utf-8",
            )
            az.chmod(0o700)
            result = subprocess.run(
                ["bash", str(_shared.ACCELERATOR / "scripts/deploy.sh"), "offline-test", "eastus2", "test01"],
                env={**os.environ, "PATH": f"{directory}:{os.environ['PATH']}", "AZ_TEST_LOG": str(log)},
                capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cannot resolve the signed-in user", result.stderr)
            self.assertEqual(log.read_text().splitlines(), ["ad signed-in-user show --query id -o tsv"])


class ModelComparisonTests(unittest.TestCase):
    def test_context_respects_fixture_roles(self):
        coordinator = compare_models.build_context({"role_groups": ["returns-coordinators"]})
        supervisor = compare_models.build_context({"role_groups": ["returns-supervisors"]})
        self.assertIn("RET-POL-2026-01", coordinator)
        self.assertNotIn("RET-SUP-2026-01", coordinator)
        self.assertIn("RET-SUP-2026-01", supervisor)
        with self.assertRaisesRegex(ValueError, "role_groups"):
            compare_models.build_context({"id": "no-role"})

    def test_refusal_must_be_exact(self):
        case = {"expected_behavior": "refuse"}
        self.assertTrue(compare_models.score_case(case, compare_models.ABSTENTION)["abstained"])
        for answer in ("", compare_models.ABSTENTION + " But the threshold is 100."):
            self.assertFalse(compare_models.score_case(case, answer)["abstained"])

    def test_citations_require_brackets_and_reject_superseded_sources(self):
        case = {
            "expected_behavior": "answer",
            "expected_citations": ["current"],
            "forbidden_citations": ["superseded"],
        }
        self.assertTrue(compare_models.score_case(case, "Answer [current]")["grounded"])
        for answer in ("current", "[current] [superseded]"):
            self.assertFalse(compare_models.score_case(case, answer)["grounded"])
        self.assertFalse(compare_models.score_case({"expected_behavior": "answer"}, "")["grounded"])

    def test_nearest_rank_p95_of_seven_is_the_maximum(self):
        response = SimpleNamespace(output_text=compare_models.ABSTENTION, usage=None)
        client = SimpleNamespace(responses=SimpleNamespace(create=lambda **kwargs: response))
        project = SimpleNamespace(get_openai_client=lambda: client)
        cases = [{"question": "test", "expected_behavior": "refuse"}] * 7
        clock = [value for i in range(1, 8) for value in (i * 10, i * 10 + i)]
        with patch.object(compare_models, "build_context", return_value="fixture"), patch.object(
            compare_models.time, "perf_counter", side_effect=clock
        ):
            row = compare_models.run_candidate(project, "test", cases)
        self.assertEqual(row["p50"], 4000)
        self.assertEqual(row["p95"], 7000)
        self.assertEqual(row["abstained"], "7/7")


class GroundedAnswerTests(unittest.TestCase):
    def test_empty_or_extended_refusal_fails(self):
        identity = ModuleType("azure.identity")
        identity.DefaultAzureCredential = lambda: object()
        knowledgebases = ModuleType("azure.search.documents.knowledgebases")
        knowledgebases.KnowledgeBaseRetrievalClient = lambda **kwargs: object()
        for text, expected_failure in (
            (grounded_answer.ABSTENTION, False),
            ("", True),
            (grounded_answer.ABSTENTION + " Here are private notes.", True),
        ):
            with self.subTest(text=text), patch.dict(
                "sys.modules",
                {"azure.identity": identity, "azure.search.documents.knowledgebases": knowledgebases},
            ), patch.object(grounded_answer, "answer", return_value=text), contextlib.redirect_stdout(io.StringIO()):
                failures = []
                grounded_answer.verify_live(
                    {"AZURE_SEARCH_ENDPOINT": "https://unused.invalid"},
                    "test", [{"id": "refusal", "question": "test", "expected_behavior": "refuse"}],
                    None, 1.0, failures,
                )
                self.assertEqual(bool(failures), expected_failure)


class FixtureTests(unittest.TestCase):
    def test_probe_markers_exist_in_the_corpus(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (_shared.ACCELERATOR / "sample-data").glob("*.md")
            if path.name != "README.md"
        ).lower()
        permission_plan = json.loads((_shared.ACCELERATOR / "permission-probe.json").read_text())
        surface_plan = json.loads((_shared.ACCELERATOR / "surface-probe.json").read_text())
        self.assertEqual(probe_permissions.validate_plan(permission_plan), [])
        self.assertEqual(probe_surface.validate_plan(surface_plan), [])
        markers = [
            marker for case in permission_plan["cases"]
            for field in ("expect_visible", "expect_hidden") for marker in case[field]
        ]
        markers.extend(
            marker for expectation in surface_plan["callers"].values()
            for field in ("response_must_contain", "response_must_not_contain")
            for marker in expectation.get(field, [])
        )
        for marker in markers:
            self.assertIn(marker.lower(), corpus)


if __name__ == "__main__":
    unittest.main()
