"""Published-schema pairing and documented fail-closed override boundaries."""
import copy
import json
from pathlib import Path
import unittest

import jsonschema

from scripts.validate_pitch_review_package import validate_review_package
from test_validate_pitch_review_package import valid_package

ROOT = Path(__file__).resolve().parents[1]
GROUPS = ('Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon')


class SchemaRoleBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / 'agents/schemas/pitch-review.schema.json').read_text())
        jsonschema.Draft202012Validator.check_schema(cls.schema)
        cls.validator = jsonschema.Draft202012Validator(cls.schema)

    def test_each_assigned_role_group_pair_is_schema_valid(self):
        package = valid_package()
        for group in GROUPS:
            with self.subTest(group=group):
                self.assertTrue(self.validator.is_valid(package['level_reviews'][group]))

    def test_every_mismatched_role_group_pair_is_schema_invalid(self):
        package = valid_package()
        for group in GROUPS:
            for wrong_group in GROUPS:
                if wrong_group == group:
                    continue
                with self.subTest(role_group=group, wrong_group=wrong_group):
                    record = copy.deepcopy(package['level_reviews'][group])
                    record['group'] = wrong_group
                    self.assertFalse(self.validator.is_valid(record))

    def test_teacher_override_metadata_cannot_bypass_non_pass(self):
        for verdict in ('REVISE', 'REJECT'):
            with self.subTest(verdict=verdict):
                package = valid_package()
                package['level_reviews']['Alpha']['verdict'] = verdict
                package['teacher_override'] = {'group': 'Alpha', 'approved': True, 'reason': 'Teacher requested release'}
                self.assertEqual(validate_review_package(package)['status'], 'FAIL')

    def test_override_documentation_states_no_bypass(self):
        orchestration = (ROOT / 'references/agent-orchestration.md').read_text()
        self.assertIn('no teacher-override input', orchestration)
        self.assertIn('does not waive', orchestration)
