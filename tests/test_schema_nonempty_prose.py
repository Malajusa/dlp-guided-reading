"""Nonempty review prose uses the production validator's Unicode strip rule."""
import json
from pathlib import Path
import unittest

import jsonschema

from test_validate_pitch_review_package import DIMS, valid_package
from scripts.validate_pitch_review_package import validate_review_package

SCHEMA_DIR = Path(__file__).resolve().parents[1] / 'agents' / 'schemas'
# Python str.strip whitespace, including C0 separators and Unicode spaces.
WHITESPACE = '\t\n\v\f\r\x1c\x1d\x1e\x1f \x85\xa0\u1680' + ''.join(
    chr(codepoint) for codepoint in range(0x2000, 0x200b)
) + '\u2028\u2029\u202f\u205f\u3000'


class SchemaNonemptyProseTests(unittest.TestCase):
    def assert_prose_matches_strip(self, kind, field, dimension=None):
        schema = json.loads((SCHEMA_DIR / f'{kind}-review.schema.json').read_text())
        validator = jsonschema.Draft202012Validator(schema)
        values = ['', *WHITESPACE, WHITESPACE, ' ' + WHITESPACE + ' ',
                  'Evidence supports the judgement.', '\t Evidence \u3000',
                  '\u200b', '\ufeff', '\x00']
        for value in values:
            package = valid_package()
            review = (package['level_reviews']['Alpha'] if kind == 'pitch'
                      else package['progression_review'])
            if dimension is None:
                review[field] = value
            else:
                review[field][dimension] = value
            expected = bool(value.strip())
            with self.subTest(kind=kind, field=field, dimension=dimension,
                              value=ascii(value)):
                self.assertEqual(validate_review_package(package)['status'],
                                 'PASS' if expected else 'FAIL')
                self.assertEqual(validator.is_valid(review), expected)

    def test_level_summary_requires_non_whitespace(self):
        self.assert_prose_matches_strip('pitch', 'pitch_summary')

    def test_progression_summary_requires_non_whitespace(self):
        self.assert_prose_matches_strip('progression', 'pitch_progression_summary')

    def test_each_dimension_finding_requires_non_whitespace(self):
        for dimension in DIMS:
            self.assert_prose_matches_strip('pitch', 'dimension_findings', dimension)
