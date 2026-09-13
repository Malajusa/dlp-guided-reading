from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SkillPitchGateContracts(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_orchestration_order_and_isolation(self):
        text = self.read("references/agent-orchestration.md")
        for phrase in (
            "weekly blueprint", "central passage writer", "five level reviewers",
            "progression/parity", "final question writing", "PowerPoint layout",
            "parallel preferred", "sequential fallback", "neighbouring candidate passages",
            "three revision cycles", "SHA-256", "stale approvals",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_skill_makes_pitch_gate_mandatory(self):
        text = self.read("SKILL.md")
        self.assertIn("Gate passage pitch before final questions", text)
        self.assertIn("references/agent-orchestration.md", text)
        self.assertIn("five current level PASS", text)
        self.assertIn("progression/parity PASS", text)
        self.assertIn("stale", text.lower())
        self.assertIn("before PowerPoint layout", text)

    def test_production_standard_release_gate(self):
        text = self.read("references/production-standard.md")
        for phrase in (
            "version 2.2", "five current level", "passage hash", "progression/parity",
            "stale", "three revision cycles", "teacher override", "question records",
            "validate_pitch_review_package.py",
        ):
            self.assertIn(phrase.lower(), text.lower())

    def test_powerpoint_contract_retains_review_evidence(self):
        text = self.read("references/powerpoint-pack-contract.md")
        for phrase in (
            "passage_sha256", "revision_cycle", "pitch_review", "progression_review",
            "pitch-review-audit.json", "validate_pitch_review_package.py",
            "teacher override", "question records", "three revision cycles",
        ):
            self.assertIn(phrase.lower(), text.lower())


if __name__ == "__main__":
    unittest.main()
