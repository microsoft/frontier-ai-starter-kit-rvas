"""Offline regression checks for the activity harnesses."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FOUNDATIONS = load_module("foundations_checks", "activities/foundations/validate.py")
BOOTSTRAP = load_module("bootstrap_checks", "scripts/validate-foundations.py")
EVALUATE = load_module("evaluation_harness", "activities/advanced-evaluation-redteam/evaluate.py")
EVAL_CHECKS = load_module("evaluation_checks", "activities/advanced-evaluation-redteam/validate.py")
ACTION_CHECKS = load_module("action_checks", "activities/advanced-action-tools/validate.py")


class ActivityRegressionTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.enterContext(contextlib.redirect_stdout(self.output))
        self.enterContext(contextlib.redirect_stderr(self.output))
        self.temp = Path(self.enterContext(tempfile.TemporaryDirectory()))

    def run_evaluation(self, rows, *args):
        dataset = self.temp / "eval.jsonl"
        dataset.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        with patch.object(sys, "argv", ["evaluate.py", "--dataset", str(dataset),
                                       "--dry-run", "--custom-only", *args]):
            return EVALUATE.main()

    def test_azd_quoted_env_and_shell_precedence(self):
        (self.temp / ".env").write_text(
            'AZURE_AI_PROJECT_ENDPOINT="https://example.invalid/api/projects/demo"\n'
            "AZURE_SEARCH_INDEX_NAME='faq'\n"
            'AZURE_AI_MODEL_DEPLOYMENT_NAME="file-model"\n',
            encoding="utf-8",
        )
        with patch.object(BOOTSTRAP, "REPO_ROOT", self.temp), patch.dict(
            os.environ, {"AZURE_AI_MODEL_DEPLOYMENT_NAME": "shell-model"}, clear=True
        ):
            env = BOOTSTRAP.load_env()
        self.assertEqual(env["AZURE_AI_PROJECT_ENDPOINT"], "https://example.invalid/api/projects/demo")
        self.assertEqual(env["AZURE_SEARCH_INDEX_NAME"], "faq")
        self.assertEqual(env["AZURE_AI_MODEL_DEPLOYMENT_NAME"], "shell-model")

    def test_bootstrap_rejects_placeholder_before_sdk_import(self):
        env = dict.fromkeys(
            ("AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_INDEX_NAME",
             "AZURE_AI_PROJECT_ENDPOINT", "AZURE_AI_MODEL_DEPLOYMENT_NAME"),
            "<placeholder>",
        )
        with patch.object(BOOTSTRAP, "load_env", return_value=env), patch.object(
            sys, "argv", ["validate-foundations.py"]
        ):
            self.assertEqual(BOOTSTRAP.main(), 1)
        self.assertIn("Missing required vars", self.output.getvalue())

    def test_agent_lookup_preserves_service_error(self):
        def forbidden():
            raise RuntimeError("access denied")

        project = SimpleNamespace(agents=SimpleNamespace(list=forbidden))
        with self.assertRaisesRegex(RuntimeError, "access denied"):
            FOUNDATIONS._find_agent(project, "missing")

    def check_grounding(self, agents, response=None):
        project = SimpleNamespace(
            agents=SimpleNamespace(list=lambda: agents),
            get_openai_client=lambda: SimpleNamespace(
                responses=SimpleNamespace(create=lambda **kwargs: response)
            ),
        )
        projects = SimpleNamespace(AIProjectClient=lambda **kwargs: project)
        env = {
            "AZURE_AI_PROJECT_ENDPOINT": "https://example.invalid",
            "AZURE_SEARCH_ENDPOINT": "https://search.invalid",
            "AZURE_SEARCH_INDEX_NAME": "faq",
        }
        with patch.dict(sys.modules, {"azure.ai.projects": projects}), patch.object(
            FOUNDATIONS, "_credential", return_value=object()
        ):
            return FOUNDATIONS.check_step4(env, False, "question")

    def test_missing_agent_returns_explicit_failure(self):
        self.assertIs(self.check_grounding([]), False)
        self.assertIn("not found", self.output.getvalue())

    def test_empty_answer_with_citation_fails(self):
        response = SimpleNamespace(
            output_text="",
            output=[SimpleNamespace(content=[SimpleNamespace(
                annotations=[SimpleNamespace(type="file_citation")]
            )])],
        )
        self.assertIs(self.check_grounding(
            [SimpleNamespace(name="sample-iq-assistant")], response
        ), False)

    def test_cited_answer_still_passes(self):
        response = SimpleNamespace(output_text="See financial-aid.md.", output=[])
        self.assertIs(self.check_grounding(
            [SimpleNamespace(name="sample-iq-assistant")], response
        ), True)

    def test_empty_dataset_cannot_pass_gate(self):
        self.assertEqual(self.run_evaluation([], "--gate", "3.5"), 2)

    def test_invalid_gate_values(self):
        for gate in ("nan", "inf", "-inf", "0", "5.1"):
            with self.subTest(gate=gate), self.assertRaises(SystemExit) as error:
                self.run_evaluation([], f"--gate={gate}")
            self.assertEqual(error.exception.code, 2)

    def test_valid_gate_pass_and_fail(self):
        rows = [{"query": "deadline?", "ground_truth": "Priority deadline March 1."}]
        self.assertEqual(self.run_evaluation(rows, "--gate", "4"), 0)
        self.assertEqual(self.run_evaluation(rows, "--gate", "5"), 1)

    def test_non_finite_score_cannot_pass_gate(self):
        class NonFiniteEvaluator:
            def __call__(self, **kwargs):
                return {"sample_domain_score": float("nan")}

        with patch.object(EVALUATE, "SampleOrganizationDomainEvaluator", NonFiniteEvaluator):
            self.assertEqual(self.run_evaluation(
                [{"query": "deadline?", "ground_truth": "March 1."}], "--gate", "3.5"
            ), 1)

    def test_foreign_email_domain_is_exact(self):
        evaluator = EVALUATE.SampleOrganizationDomainEvaluator()
        for email in ("help@sample.edu.example", "sample.edu@evil.example"):
            result = evaluator(query="contact?", response=email, ground_truth="help@sample.edu")
            self.assertIn("hallucinated/foreign contact", result["sample_reason"])
        result = evaluator(query="contact?", response="Email help@sample.edu.",
                           ground_truth="Email help@sample.edu.")
        self.assertNotIn("hallucinated/foreign contact", result["sample_reason"])

    def test_adversarial_set_requires_three_categories(self):
        dataset = self.temp / "adversarial.jsonl"
        rows = [{"category": "jailbreak", "injected_context": "test",
                 "expected_behavior": "decline"} for _ in range(5)]
        dataset.write_text("\n".join(map(json.dumps, rows)), encoding="utf-8")
        self.assertFalse(EVAL_CHECKS.check_step4(dataset, "reference"))
        rows[0]["category"] = "harmful-content"
        rows[1]["category"] = "indirect-prompt-injection"
        dataset.write_text("\n".join(map(json.dumps, rows)), encoding="utf-8")
        self.assertTrue(EVAL_CHECKS.check_step4(dataset, "reference"))

    def test_stale_ticket_cannot_pass_action_checkpoint(self):
        wiring = self.temp / "wiring.py"
        wiring.write_text(
            "def run_with_approval(client, agent_name, prompt):\n"
            "    conversation = client.conversations.create()\n"
            "    client.responses.create(conversation=conversation.id, input=prompt)\n"
            "    client.responses.create(conversation=conversation.id,\n"
            "        input=[{'call_id': 'validation-call-1', 'output': 'no action'}])\n",
            encoding="utf-8",
        )
        stale = {"student_id": "validate_py", "summary": "checkpoint smoke ticket",
                 "ticket_id": "INC-OLD"}
        httpx = SimpleNamespace(get=lambda *args, **kwargs: SimpleNamespace(
            raise_for_status=lambda: None, json=lambda: {"items": [stale]}
        ))
        with patch.object(ACTION_CHECKS, "WIRING", wiring), patch.dict(
            sys.modules, {"httpx": httpx}
        ):
            self.assertFalse(ACTION_CHECKS.check_step4())
        self.assertIn("did not create", self.output.getvalue())


if __name__ == "__main__":
    unittest.main()
