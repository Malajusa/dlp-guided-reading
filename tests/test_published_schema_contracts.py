"""Persistent shape checks for every published pitch/orchestration schema."""
import copy
import json
from pathlib import Path
import unittest

import jsonschema

from test_validate_pitch_review_package import valid_package
from scripts.validate_pitch_review_package import canonical_passage_hash

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / 'agents' / 'schemas'


def valid_state():
    package = valid_package()
    return {
        'schema_version': '1.0',
        'groups': {
            group: {
                'text': passage['text'],
                'current_sha256': canonical_passage_hash(passage['text']),
                'revision_cycle': 0,
                'level_review_status': 'PASS',
                'question_records_valid': False,
            }
            for group, passage in package['passages'].items()
        },
        'progression_review_status': 'PASS',
    }


class PublishedSchemaContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            path.name: json.loads(path.read_text(encoding='utf-8'))
            for path in SCHEMA_DIR.glob('*.schema.json')
        }

    def validator(self, name):
        return jsonschema.Draft202012Validator(self.schemas[name + '.schema.json'])

    def test_all_published_schemas_are_well_formed(self):
        self.assertTrue({'pitch-review.schema.json', 'progression-review.schema.json',
                         'orchestration-state.schema.json'} <= set(self.schemas))
        for name, schema in self.schemas.items():
            with self.subTest(schema=name):
                jsonschema.Draft202012Validator.check_schema(schema)

    def test_progression_accepts_representative_record(self):
        self.assertTrue(self.validator('progression-review').is_valid(
            valid_package()['progression_review']))

    def test_progression_rejects_malformed_records(self):
        original = valid_package()['progression_review']
        missing_hash = copy.deepcopy(original)
        del missing_hash['passage_sha256']['Beta']
        bad_verdict = copy.deepcopy(original)
        bad_verdict['verdict'] = 'APPROVED'
        bad_hash = copy.deepcopy(original)
        bad_hash['passage_sha256']['Alpha'] = 'not-a-sha256'
        wrong_revision_type = copy.deepcopy(original)
        wrong_revision_type['required_revisions'] = {'Gamma': [42]}
        extra_field = copy.deepcopy(original)
        extra_field['unexpected'] = True
        for name, record in [('missing_hash', missing_hash), ('bad_verdict', bad_verdict),
                             ('bad_hash', bad_hash), ('wrong_revision_type', wrong_revision_type),
                             ('extra_field', extra_field)]:
            with self.subTest(case=name):
                self.assertFalse(self.validator('progression-review').is_valid(record))

    def test_orchestration_accepts_representative_states_and_cycle_boundaries(self):
        for cycle in (0, 3):
            state = valid_state()
            state['groups']['Alpha']['revision_cycle'] = cycle
            with self.subTest(cycle=cycle):
                self.assertTrue(self.validator('orchestration-state').is_valid(state))

    def test_orchestration_rejects_malformed_states(self):
        cases = []
        for cycle in (-1, 4, True):
            state = valid_state()
            state['groups']['Alpha']['revision_cycle'] = cycle
            cases.append((f'cycle_{cycle}', state))
        wrong_boolean = valid_state()
        wrong_boolean['groups']['Alpha']['question_records_valid'] = 'true'
        cases.append(('wrong_boolean', wrong_boolean))
        missing_group = valid_state()
        del missing_group['groups']['Beta']
        cases.append(('missing_group', missing_group))
        wrong_status = valid_state()
        wrong_status['progression_review_status'] = 'APPROVED'
        cases.append(('wrong_status', wrong_status))
        bad_hash = valid_state()
        bad_hash['groups']['Alpha']['current_sha256'] = 'not-a-sha256'
        cases.append(('bad_hash', bad_hash))
        extra_field = valid_state()
        extra_field['unexpected'] = True
        cases.append(('extra_field', extra_field))
        for name, state in cases:
            with self.subTest(case=name):
                self.assertFalse(self.validator('orchestration-state').is_valid(state))
