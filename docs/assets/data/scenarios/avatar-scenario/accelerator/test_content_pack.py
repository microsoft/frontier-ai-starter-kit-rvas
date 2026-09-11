import json
from pathlib import Path
import shutil
import tempfile
import unittest

from content_pack import PackRejectedError, build_artifact, validate_pack


class ContentPackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data_dir = Path(self.temp.name) / "pack"
        shutil.copytree(Path(__file__).parent / "sample-data", self.data_dir)

    def test_unchanged_pack_builds_reproducibly(self):
        pack = validate_pack(self.data_dir)
        self.assertEqual(build_artifact(pack), build_artifact(pack))

    def test_artifact_metadata_must_be_nonempty_text(self):
        for filename, field in (
            ("approvals.json", "approval_record_id"),
            ("storyboard-script.json", "publication_id"),
            ("storyboard-script.json", "locale"),
        ):
            path = self.data_dir / filename
            original = path.read_text(encoding="utf-8")
            for value in (None, "", " ", 42):
                with self.subTest(field=field, value=value):
                    record = json.loads(original)
                    if value is None:
                        record.pop(field)
                    else:
                        record[field] = value
                    path.write_text(json.dumps(record), encoding="utf-8")
                    with self.assertRaisesRegex(PackRejectedError, field):
                        validate_pack(self.data_dir)
            path.write_text(original, encoding="utf-8")

    def test_matching_missing_publication_ids_do_not_pass(self):
        for filename in ("storyboard-script.json", "feedback-fixture.json"):
            path = self.data_dir / filename
            record = json.loads(path.read_text(encoding="utf-8"))
            record.pop("publication_id")
            path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaisesRegex(PackRejectedError, "publication_id"):
            validate_pack(self.data_dir)

    def test_withdrawn_pack_is_rejected(self):
        path = self.data_dir / "approvals.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["approval_status"] = "withdrawn"
        path.write_text(json.dumps(record), encoding="utf-8")
        with self.assertRaises(PackRejectedError):
            validate_pack(self.data_dir)


if __name__ == "__main__":
    unittest.main()
