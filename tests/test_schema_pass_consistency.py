"""PASS review schemas must agree with the fail-closed production gate."""
import json
from pathlib import Path
import unittest

import jsonschema

from test_validate_pitch_review_package import valid_package
from scripts.validate_pitch_review_package import validate_review_package

SCHEMA_DIR = Path(__file__).resolve().parents[1] / 'agents' / 'schemas'


class SchemaPassConsistencyTests(unittest.TestCase):
    def assert_pass_requires_empty(self, kind, field, invalid_values):
        schema = json.loads((SCHEMA_DIR / f'{kind}-review.schema.json').read_text())
        validator = jsonschema.Draft202012Validator(schema)
        for value in invalid_values:
            package = valid_package()
            review = (package['level_reviews']['Alpha'] if kind == 'pitch'
                      else package['progression_review'])
            with self.subTest(kind=kind, field=field, value=value):
                # An ordinary empty PASS record remains accepted by both checks.
                self.assertTrue(validator.is_valid(review))
                self.assertEqual(validate_review_package(package)['status'], 'PASS')
                review[field] = value
                self.assertEqual(validate_review_package(package)['status'], 'FAIL')
                self.assertFalse(validator.is_valid(review))
                # Revision/rejection records may describe unresolved work, but
                # can never release a package through the production gate.
                verdicts = (('REVISE', 'REJECT') if kind == 'pitch'
                            else ('REVISE_LEVELS', 'REJECT_SET'))
                for verdict in verdicts:
                    review['verdict'] = verdict
                    self.assertTrue(validator.is_valid(review))
                    self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_level_pass_rejects_blocking_issues(self):
        self.assert_pass_requires_empty('pitch', 'blocking_issues', [['Unresolved issue']])

    def test_level_pass_rejects_required_revisions(self):
        self.assert_pass_requires_empty('pitch', 'required_revisions', [['Required change']])

    def test_progression_pass_rejects_blocking_issues(self):
        self.assert_pass_requires_empty('progression', 'blocking_issues', [['Unresolved issue']])

    def test_progression_pass_rejects_required_revisions(self):
        self.assert_pass_requires_empty('progression', 'required_revisions', [
            {'Alpha': ['Required change']}, {'Alpha': []},
        ])
