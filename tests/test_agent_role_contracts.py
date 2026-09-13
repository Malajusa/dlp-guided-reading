from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    "Alpha": "alpha-pitch-reviewer",
    "Beta": "beta-pitch-reviewer",
    "Gamma": "gamma-pitch-reviewer",
    "Delta": "delta-pitch-reviewer",
    "Epsilon": "epsilon-pitch-reviewer",
}
DIMS = [
    "decoding", "vocabulary_morphology", "syntax", "cohesion",
    "background_knowledge", "evidence_distance", "inference_ambiguity",
    "response_demand", "age_appropriateness", "visual_support", "conceptual_parity",
]


class RoleContractTests(unittest.TestCase):
    def test_level_roles_are_group_specific_and_fail_closed(self):
        for group, role in GROUPS.items():
            text = (ROOT / "agents" / "roles" / f"{role}.md").read_text(encoding="utf-8")
            self.assertIn(f"Group: {group}", text)
            self.assertIn(f"Role id: {role}", text)
            for verdict in ("PASS", "REVISE", "REJECT"):
                self.assertIn(verdict, text)
            self.assertIn("passage_sha256", text)
            self.assertIn("must not change", text.lower())
            self.assertIn("neighbouring candidate passages", text.lower())
            for dim in DIMS:
                self.assertIn(dim, text)

    def test_writer_cannot_self_approve(self):
        text = (ROOT / "agents" / "roles" / "central-passage-writer.md").read_text(encoding="utf-8")
        self.assertIn("must not self-certify", text.lower())
        self.assertIn("does not have PASS authority", text)
        self.assertIn("three unsuccessful review cycles", text)

    def test_progression_role_contract(self):
        text = (ROOT / "agents" / "roles" / "progression-parity-reviewer.md").read_text(encoding="utf-8")
        for group in GROUPS:
            self.assertIn(group, text)
        for phrase in (
            "adjacent-group duplication", "conceptual parity", "visual-support progression",
            "difficulty jumps", "Alpha/Beta content loss", "Delta/Epsilon topic drift",
            "question-demand progression", "genuine Epsilon complexity", "REVISE_LEVELS",
            "REJECT_SET", "passage_sha256",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
