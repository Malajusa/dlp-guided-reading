import copy
import unittest

from scripts.validate_pitch_review_package import canonical_passage_hash, validate_review_package

GROUPS = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
DIMS = {
    "decoding": "pass",
    "vocabulary_morphology": "pass",
    "syntax": "pass",
    "cohesion": "pass",
    "background_knowledge": "pass",
    "evidence_distance": "pass",
    "inference_ambiguity": "pass",
    "response_demand": "pass",
    "age_appropriateness": "pass",
    "visual_support": "pass",
    "conceptual_parity": "pass",
}


def valid_package():
    passages = {g: {"text": f"Final {g} passage.", "revision_cycle": 1} for g in GROUPS}
    reviews = {}
    hashes = {}
    for g in GROUPS:
        h = canonical_passage_hash(passages[g]["text"])
        hashes[g] = h
        reviews[g] = {
            "reviewer_role": f"{g.lower()}-pitch-reviewer",
            "group": g,
            "passage_sha256": h,
            "verdict": "PASS",
            "pitch_summary": "Appropriately pitched.",
            "dimension_findings": dict(DIMS),
            "blocking_issues": [],
            "required_revisions": [],
            "non_blocking_notes": [],
        }
    return {
        "schema_version": "1.0",
        "passages": passages,
        "level_reviews": reviews,
        "progression_review": {
            "reviewer_role": "progression-parity-reviewer",
            "verdict": "PASS",
            "passage_sha256": hashes,
            "pitch_progression_summary": "Coherent progression.",
            "blocking_issues": [],
            "required_revisions": {},
            "non_blocking_notes": [],
        },
    }


class ReviewPackageTests(unittest.TestCase):
    def test_valid_package_passes(self):
        self.assertEqual(validate_review_package(valid_package())["status"], "PASS")

    def test_stale_level_hash_fails(self):
        package = valid_package()
        package["passages"]["Gamma"]["text"] += " changed"
        report = validate_review_package(package)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any("Gamma" in error and "hash" in error.lower() for error in report["errors"]))

    def test_pass_with_required_revision_fails(self):
        package = valid_package()
        package["level_reviews"]["Alpha"]["required_revisions"] = ["Remove answer giveaway."]
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_missing_group_review_fails(self):
        package = valid_package()
        del package["level_reviews"]["Beta"]
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_revision_cycle_above_three_fails(self):
        package = valid_package()
        package["passages"]["Delta"]["revision_cycle"] = 4
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_stale_progression_hash_fails(self):
        package = valid_package()
        package["progression_review"]["passage_sha256"]["Epsilon"] = "0" * 64
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_malformed_dimensions_fail(self):
        package = valid_package()
        del package["level_reviews"]["Gamma"]["dimension_findings"]["syntax"]
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_revise_verdict_fails_release_package(self):
        package = valid_package()
        package["level_reviews"]["Beta"]["verdict"] = "REVISE"
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_reject_verdict_fails_release_package(self):
        package = valid_package()
        package["level_reviews"]["Epsilon"]["verdict"] = "REJECT"
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_forbidden_placement_change_field_fails(self):
        package = valid_package()
        package["level_reviews"]["Alpha"]["replacement_profile"] = "at level"
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_parity_revise_levels_fails(self):
        package = valid_package()
        package["progression_review"]["verdict"] = "REVISE_LEVELS"
        package["progression_review"]["required_revisions"] = {"Gamma": ["Increase independence."]}
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_parity_reject_set_fails(self):
        package = valid_package()
        package["progression_review"]["verdict"] = "REJECT_SET"
        self.assertEqual(validate_review_package(package)["status"], "FAIL")

    def test_changed_passage_after_approval_fails(self):
        package = valid_package()
        original = copy.deepcopy(package["level_reviews"]["Alpha"])
        package["passages"]["Alpha"]["text"] = "Revised Alpha passage."
        package["level_reviews"]["Alpha"] = original
        self.assertEqual(validate_review_package(package)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
