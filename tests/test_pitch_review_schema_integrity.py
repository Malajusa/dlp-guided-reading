"""Regression checks for the published review schemas' fail-closed boundary."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest
from test_validate_pitch_review_package import valid_package
from scripts.validate_pitch_review_package import validate_review_package


class ReviewSchemaIntegrityTests(unittest.TestCase):
    def test_level_review_rejects_unknown_fields(self):
        package = valid_package()
        package['level_reviews']['Alpha']['unrecognised_approval'] = True
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_progression_review_rejects_unknown_fields(self):
        package = valid_package()
        package['progression_review']['unrecognised_approval'] = True
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_level_notes_require_string_items(self):
        package = valid_package()
        package['level_reviews']['Alpha']['non_blocking_notes'] = [42]
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_progression_notes_require_string_items(self):
        package = valid_package()
        package['progression_review']['non_blocking_notes'] = [{'note': 'not a string'}]
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_malformed_level_verdict_fails_without_exception(self):
        package = valid_package()
        package['level_reviews']['Alpha']['verdict'] = ['PASS']
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_malformed_progression_verdict_fails_without_exception(self):
        package = valid_package()
        package['progression_review']['verdict'] = {'value': 'PASS'}
        self.assertEqual(validate_review_package(package)['status'], 'FAIL')


class MalformedPackageCliTests(unittest.TestCase):
    def assert_fail_audit(self, raw_json):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'package.json'
            audit = Path(temp) / 'audit.json'
            source.write_text(raw_json, encoding='utf-8')
            script = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_pitch_review_package.py'
            result = subprocess.run([sys.executable, str(script), '--package', str(source), '--out', str(audit)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(audit.is_file(), 'Malformed JSON values must still produce the requested FAIL audit')
            report = json.loads(audit.read_text(encoding='utf-8'))
            self.assertEqual(report['status'], 'FAIL')
            self.assertTrue(report['errors'])

    def test_oversized_integer_writes_fail_audit(self):
        self.assert_fail_audit('{"notes": [' + '9' * 5000 + ']}')

    def test_excessive_nesting_writes_fail_audit(self):
        package = valid_package()
        package['level_reviews']['Alpha']['non_blocking_notes'] = "NESTED_NOTE"
        raw = json.dumps(package).replace('"NESTED_NOTE"', '[' * 997 + '0' + ']' * 997)
        self.assert_fail_audit(raw)
