"""Override requests are source notes, never executable release-package inputs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_validate_pitch_review_package import valid_package
from scripts.validate_pitch_review_package import validate_review_package

ROOT = Path(__file__).resolve().parents[1]


class OverrideInputContractTests(unittest.TestCase):
    def test_valid_pass_rejects_override_key_but_preserves_metadata_compatibility(self):
        package = valid_package()
        package['supplemental_metadata'] = {'run_label': 'controlled sample'}
        self.assertEqual(validate_review_package(package)['status'], 'PASS')
        for value in (None, False, {}, {'approved': True}):
            with self.subTest(value=value):
                package['teacher_override'] = value
                report = validate_review_package(package)
                self.assertEqual(report['status'], 'FAIL')
                self.assertTrue(any('teacher_override' in error for error in report['errors']))

    def test_override_key_does_not_replace_non_pass_errors(self):
        for kind, verdict in [('level', 'REVISE'), ('level', 'REJECT'),
                              ('progression', 'REVISE_LEVELS'), ('progression', 'REJECT_SET')]:
            with self.subTest(kind=kind, verdict=verdict):
                package = valid_package()
                record = (package['level_reviews']['Alpha'] if kind == 'level'
                          else package['progression_review'])
                record['verdict'] = verdict
                package['teacher_override'] = {'approved': True}
                report = validate_review_package(package)
                self.assertEqual(report['status'], 'FAIL')
                self.assertTrue(any('teacher_override' in error for error in report['errors']))
                self.assertTrue(any('requires PASS' in error for error in report['errors']))

    def test_cli_override_input_writes_fail_audit(self):
        package = valid_package()
        package['teacher_override'] = {'approved': True}
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'package.json'
            out = Path(temp) / 'audit.json'
            source.write_text(json.dumps(package), encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_pitch_review_package.py'),
                                     '--package', str(source), '--out', str(out)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(out.read_text())['status'], 'FAIL')

    def test_design_and_runtime_contract_have_no_override_execution_path(self):
        design = (ROOT / 'docs/superpowers/specs/2026-09-12-level-pitch-agent-architecture-design.md').read_text()
        orchestration = (ROOT / 'references/agent-orchestration.md').read_text()
        for text in (design, orchestration):
            self.assertIn('no teacher-override input', text)
            self.assertIn('does not waive', text)
        self.assertNotIn('or the teacher explicitly overrides it', design)
        self.assertNotIn('implementation not yet started', design)
        self.assertIn('ignored', orchestration)
        self.assertIn('teacher_override', orchestration)
