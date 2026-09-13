# Level-Specific Pitch Agent Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add five independent Alpha-Epsilon pitch-review agents, a central passage writer, and a cross-level progression/parity reviewer so no Guided Reading passage can reach final question writing or layout without valid pitch approval bound to the exact passage text.

**Architecture:** Keep role instructions in focused Markdown files, orchestration rules in one reference contract, and fail-closed approval validation in a standard-library Python script. The skill remains runtime-agnostic: parallel reviewer dispatch is preferred where supported; a sequential fallback is permitted only when reviewer information barriers are preserved. Mechanical approval integrity is enforced with SHA-256 hashes and machine-readable review records; pedagogical pitch remains the responsibility of the specialist agents.

**Tech Stack:** Markdown skill/role contracts, JSON/JSON Schema documents, Python 3 standard library (`argparse`, `hashlib`, `json`, `pathlib`, `unittest`), existing PowerPoint audit workflow.

**Spec:** `docs/superpowers/specs/2026-09-12-level-pitch-agent-architecture-design.md`

## Global Constraints

- Fixed teacher-assigned rotation remains Monday Alpha, Tuesday Beta, Wednesday Gamma, Thursday Delta, Friday Epsilon.
- Teacher-assigned profiles are authoritative; agents must not assess students, infer placements, or change groups.
- Alpha-Epsilon keep the same age-appropriate Year 4/5 conceptual destination; complexity changes through genuine rewrites.
- Epsilon means Year 9 reading complexity applied to Year 4/5 subject matter, not Year 9 curriculum content.
- Student-facing material shows only Greek group names, never assessed levels or profile descriptions.
- A passage writer must never approve its own pitch.
- Level reviewers initially see only their assigned candidate passage plus profile/reference context; they do not see neighbouring draft passages or other level-review verdicts.
- Level verdicts are exactly `PASS`, `REVISE`, or `REJECT` and are bound to the exact candidate text by SHA-256.
- A `PASS` is invalid if `blocking_issues` or `required_revisions` is non-empty.
- Maximum normal revision loop is three cycles per passage; a fourth unsuccessful review requires fresh redrafting rather than continued patching.
- Progression/parity review runs only after five valid level `PASS` records and is bound to the exact five passage hashes.
- Any wording change invalidates that level's prior approval; any change to any passage invalidates prior parity approval.
- Passage changes that affect evidence locations or answerability invalidate dependent question records and require question/evidence QA again.
- Pitch review does not replace factual/cultural QA, the 40-week overview, NAPLAN-informed question QA, PowerPoint structural audit, or rendered visual inspection.
- Use only Python standard library for new deterministic validation, matching `scripts/audit_reading_pack.py`.

---

## File Map

**Create**
- `agents/roles/central-passage-writer.md` — drafting/revision authority, never approval.
- `agents/roles/alpha-pitch-reviewer.md` — Alpha-only approval contract.
- `agents/roles/beta-pitch-reviewer.md` — Beta-only approval contract.
- `agents/roles/gamma-pitch-reviewer.md` — Gamma-only approval contract.
- `agents/roles/delta-pitch-reviewer.md` — Delta-only approval contract.
- `agents/roles/epsilon-pitch-reviewer.md` — Epsilon-only approval contract.
- `agents/roles/progression-parity-reviewer.md` — side-by-side five-text gate.
- `agents/schemas/pitch-review.schema.json` — machine-readable level-review contract.
- `agents/schemas/progression-review.schema.json` — machine-readable parity-review contract.
- `agents/schemas/orchestration-state.schema.json` — working-state contract for passages, cycles, approvals and invalidation flags.
- `references/agent-orchestration.md` — runtime-neutral dispatch, isolation, revision and gate sequence.
- `scripts/validate_pitch_review_package.py` — fail-closed hash/record validator.
- `tests/test_validate_pitch_review_package.py` — validator unit tests.
- `tests/test_agent_role_contracts.py` — static role-contract tests.
- `tests/test_skill_pitch_gate_contracts.py` — static cross-document contract tests.
- `tests/fixtures/pitch-agent-cases.json` — adversarial/positive behaviour cases.
- `docs/validation/level-pitch-agent-validation.md` — recorded behavioural and forward-test evidence.

**Modify**
- `SKILL.md` — insert the writer → five reviewers → parity gate before final question writing/layout.
- `references/production-standard.md` — make missing/stale pitch approvals blocking failures.
- `references/powerpoint-pack-contract.md` — require pitch-review artefacts/hashes in the working source record and final manual gate.

**Do not modify in this feature**
- `references/40-week-reading-overview.md`
- `references/group-profiles.md` except only if implementation reveals a contradiction; otherwise treat it as authoritative input.
- `references/naplan-reading-question-design.md`
- `scripts/audit_reading_pack.py` — keep semantic pitch QA separate from PPTX structural auditing.
- `agents/openai.yaml` unless a final review shows the current entry-point description no longer discovers the skill correctly.

---

### Task 1: Add fail-closed review data contracts and validator

**Files:**
- Create: `agents/schemas/pitch-review.schema.json`
- Create: `agents/schemas/progression-review.schema.json`
- Create: `agents/schemas/orchestration-state.schema.json`
- Create: `scripts/validate_pitch_review_package.py`
- Create: `tests/test_validate_pitch_review_package.py`

**Interfaces:**
- Consumes: one JSON package containing exact passage text, per-level review records, revision-cycle counts, and progression review.
- Produces: `canonical_passage_hash(text: str) -> str`, `validate_review_package(package: dict) -> dict`, and CLI exit code `0` only when every gate is current and passing.
- CLI: `python scripts/validate_pitch_review_package.py --package <pitch-review-package.json> --out <pitch-review-audit.json>`.

- [ ] **Step 1: Write failing validator tests**

Create `tests/test_validate_pitch_review_package.py` using `unittest`. Include helpers and at least these failures before implementation:

```python
import copy
import unittest

from scripts.validate_pitch_review_package import (
    canonical_passage_hash,
    validate_review_package,
)

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
        report = validate_review_package(valid_package())
        self.assertEqual(report["status"], "PASS")

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
```

- [ ] **Step 2: Run the test module and confirm RED**

Run:

```bash
python -m unittest tests.test_validate_pitch_review_package -v
```

Expected: import failure because `scripts/validate_pitch_review_package.py` does not exist yet.

- [ ] **Step 3: Implement the minimal validator**

Create `scripts/validate_pitch_review_package.py` with standard-library-only logic. Core signatures:

```python
EXPECTED_GROUPS = ("Alpha", "Beta", "Gamma", "Delta", "Epsilon")
REQUIRED_DIMENSIONS = (
    "decoding", "vocabulary_morphology", "syntax", "cohesion",
    "background_knowledge", "evidence_distance", "inference_ambiguity",
    "response_demand", "age_appropriateness", "visual_support",
    "conceptual_parity",
)
FORBIDDEN_REVIEW_FIELDS = {"suggested_profile", "replacement_profile", "new_group"}


def canonical_passage_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_review_package(package: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    # Require schema_version 1.0, exactly five groups, cycles 0..3.
    # Recompute passage hashes from exact text.
    # Require one PASS review per group with correct reviewer role and hash.
    # PASS cannot contain blocking_issues or required_revisions.
    # Require all dimension findings and reject placement-change fields.
    # Require progression PASS whose five hashes exactly match current passages.
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}
```

Add CLI parsing with `--package` and `--out`, write a JSON report, print it, and return exit `1` on `FAIL`.

- [ ] **Step 4: Add the three JSON Schema reference contracts**

`pitch-review.schema.json` must set `additionalProperties: false`, require the exact role/group/hash/verdict/summary/dimensions/list fields, restrict verdict to `PASS|REVISE|REJECT`, and require a 64-character lowercase hex hash.

`progression-review.schema.json` must require all five hashes and verdict `PASS|REVISE_LEVELS|REJECT_SET`.

`orchestration-state.schema.json` must define exactly five group entries, `revision_cycle` integer `0..3`, candidate `text`, current hash, level-review status, `question_records_valid` boolean, and progression-review status.

- [ ] **Step 5: Run validator tests and confirm GREEN**

Run:

```bash
python -m unittest tests.test_validate_pitch_review_package -v
```

Expected: all tests pass.

- [ ] **Step 6: Add additional fail-closed tests**

Add tests for malformed dimensions, `REVISE`, `REJECT`, forbidden placement-change fields, parity `REVISE_LEVELS`, parity `REJECT_SET`, and a passage modified after approval. Re-run full module.

- [ ] **Step 7: Commit Task 1**

```bash
git add agents/schemas scripts/validate_pitch_review_package.py tests/test_validate_pitch_review_package.py
git commit -m "feat: validate level pitch approvals fail closed"
```

---

### Task 2: Define the central writer and five independent level reviewers

**Files:**
- Create: `agents/roles/central-passage-writer.md`
- Create: `agents/roles/alpha-pitch-reviewer.md`
- Create: `agents/roles/beta-pitch-reviewer.md`
- Create: `agents/roles/gamma-pitch-reviewer.md`
- Create: `agents/roles/delta-pitch-reviewer.md`
- Create: `agents/roles/epsilon-pitch-reviewer.md`
- Create: `tests/test_agent_role_contracts.py`

**Interfaces:**
- Writer consumes the weekly blueprint and outputs five candidate passages; it never emits approval verdicts.
- Each level reviewer consumes only its assigned candidate passage + specified context and emits one `pitch-review.schema.json`-compatible object.

- [ ] **Step 1: Write failing static role-contract tests**

Create `tests/test_agent_role_contracts.py` that asserts every reviewer file exists and contains its unique group, expected reviewer role id, exact verdict vocabulary, the eleven required dimensions, `passage_sha256`, the no-placement-change rule, and the information barrier.

Example:

```python
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

class RoleContractTests(unittest.TestCase):
    def test_level_roles_are_group_specific_and_fail_closed(self):
        for group, role in GROUPS.items():
            text = (ROOT / "agents" / "roles" / f"{role}.md").read_text(encoding="utf-8")
            self.assertIn(f"Group: {group}", text)
            self.assertIn("PASS", text)
            self.assertIn("REVISE", text)
            self.assertIn("REJECT", text)
            self.assertIn("passage_sha256", text)
            self.assertIn("must not change", text.lower())
            self.assertIn("neighbouring candidate passages", text.lower())
```

Also assert the central writer file contains `must not self-certify` and does not grant itself `PASS` authority.

- [ ] **Step 2: Run tests and confirm RED**

Run:

```bash
python -m unittest tests.test_agent_role_contracts -v
```

Expected: file-not-found failures.

- [ ] **Step 3: Write `central-passage-writer.md`**

Define inputs, outputs, non-negotiable common conceptual spine, genuine rewrite dimensions, revision behaviour, and explicit prohibition on self-approval. Include this decision rule:

```text
If a reviewer requests a local repair, revise only that passage unless the issue exposes a shared factual/conceptual defect. Any wording change invalidates the previous passage hash and approval. After three unsuccessful review cycles, redraft from the blueprint rather than patch again.
```

- [ ] **Step 4: Write the five reviewer role files**

Use the approved spec language for each profile. Every role file must include:

1. role id and fixed group;
2. authority boundary;
3. exact input list;
4. information it must not receive;
5. common eleven-dimension review checklist;
6. group-specific positive expectations;
7. group-specific blocking examples;
8. exact output JSON shape;
9. verdict rules;
10. instruction to review the exact text and bind the result to its SHA-256;
11. instruction to return specific revision requirements without taking over authorship.

Do not copy neighbouring candidate text into a level role prompt. Boundary comparison must use `references/group-profiles.md` profile definitions only.

- [ ] **Step 5: Run role tests and confirm GREEN**

```bash
python -m unittest tests.test_agent_role_contracts -v
```

Expected: pass.

- [ ] **Step 6: Commit Task 2**

```bash
git add agents/roles tests/test_agent_role_contracts.py
git commit -m "feat: add independent Alpha-Epsilon pitch reviewers"
```

---

### Task 3: Add the progression/parity reviewer

**Files:**
- Create: `agents/roles/progression-parity-reviewer.md`
- Modify: `tests/test_agent_role_contracts.py`

**Interfaces:**
- Consumes only five individually approved passages, their current hashes, visual plans, profile definitions, conceptual spine, and provisional question-intent targets.
- Produces a `progression-review.schema.json`-compatible object with verdict `PASS`, `REVISE_LEVELS`, or `REJECT_SET`.

- [ ] **Step 1: Add a failing parity-role test**

Assert the file requires all five groups/hashes, checks adjacent duplication, conceptual parity, visual-support progression, difficulty jumps, Alpha/Beta content loss, Delta/Epsilon topic drift, question-demand progression, and genuine Epsilon complexity.

- [ ] **Step 2: Run test and confirm RED**

```bash
python -m unittest tests.test_agent_role_contracts.RoleContractTests.test_progression_role_contract -v
```

Expected: missing file/failing required phrases.

- [ ] **Step 3: Implement `progression-parity-reviewer.md`**

The role must explicitly state:

```text
You may add revision requirements but may not override a failed level reviewer. Review only after all five level approvals are valid. Bind your verdict to all five exact passage hashes. If any passage changes later, this approval expires.
```

Define `REVISE_LEVELS` output as a mapping of group names to concrete revision requirements and `REJECT_SET` for systemic blueprint/writer failure.

- [ ] **Step 4: Run role tests and confirm GREEN**

```bash
python -m unittest tests.test_agent_role_contracts -v
```

- [ ] **Step 5: Commit Task 3**

```bash
git add agents/roles/progression-parity-reviewer.md tests/test_agent_role_contracts.py
git commit -m "feat: add cross-level progression and parity gate"
```

---

### Task 4: Implement runtime-neutral orchestration and wire it into the skill

**Files:**
- Create: `references/agent-orchestration.md`
- Modify: `SKILL.md`
- Create: `tests/test_skill_pitch_gate_contracts.py`

**Interfaces:**
- Orchestration consumes the weekly blueprint and role files.
- Orchestration produces five current level `PASS` records + one current parity `PASS` before final question writing/layout.
- Parallel reviewer dispatch is preferred; isolated sequential fallback is permitted.

- [ ] **Step 1: Write failing orchestration contract tests**

Create tests that require `SKILL.md` and `references/agent-orchestration.md` to state the order:

```text
blueprint -> central writer -> five level reviewers -> revisions until PASS -> progression/parity -> final question writing -> layout
```

Also assert that `SKILL.md` blocks layout when approvals are missing/stale and that the orchestration reference requires reviewer isolation and max three review cycles.

- [ ] **Step 2: Run tests and confirm RED**

```bash
python -m unittest tests.test_skill_pitch_gate_contracts -v
```

- [ ] **Step 3: Write `references/agent-orchestration.md`**

Specify these stages exactly:

1. resolve weekly blueprint and provisional question-intent targets;
2. central writer drafts all five;
3. compute exact SHA-256 for each passage;
4. dispatch five reviewers independently (parallel preferred);
5. validate reviewer JSON before accepting verdict;
6. send only required revisions + original blueprint back to writer;
7. re-hash changed passages and invalidate stale approvals;
8. after five current passes, dispatch progression/parity reviewer;
9. validate parity hashes;
10. only then write/finalise question records;
11. if passage text changes during question QA, return to the affected level review and then parity review;
12. only approved/current text proceeds to PowerPoint layout.

Define sequential fallback as separate reviewer calls with no neighbouring drafts or prior verdicts in context.

- [ ] **Step 4: Modify `SKILL.md`**

Add `references/agent-orchestration.md` to the references list and insert a concise `## Gate passage pitch before final questions` section before `## Design questions deliberately`.

The section must make the agent workflow mandatory for full weekly generation, while allowing a clearly labelled development fallback when the runtime cannot dispatch independent agents. That fallback must still use isolated role invocations and the same fail-closed review records; it may not collapse writer and reviewer into one self-approving pass.

- [ ] **Step 5: Run orchestration tests and confirm GREEN**

```bash
python -m unittest tests.test_skill_pitch_gate_contracts -v
```

- [ ] **Step 6: Commit Task 4**

```bash
git add references/agent-orchestration.md SKILL.md tests/test_skill_pitch_gate_contracts.py
git commit -m "feat: gate passage generation through pitch agents"
```

---

### Task 5: Make pitch approval a production and source-record release gate

**Files:**
- Modify: `references/production-standard.md`
- Modify: `references/powerpoint-pack-contract.md`
- Modify: `tests/test_skill_pitch_gate_contracts.py`

**Interfaces:**
- Working source record must retain current passage hashes, level review records, revision cycles, parity review, and explicit teacher overrides.
- Release blocks if mechanical validator is not `PASS` or if a passage changed after its recorded review.

- [ ] **Step 1: Add failing cross-document tests**

Require both documents to mention:
- five current level passes;
- exact passage hash binding;
- progression/parity pass;
- stale approval invalidation;
- max three revision cycles;
- teacher override record;
- question-record invalidation after passage edits.

- [ ] **Step 2: Run tests and confirm RED**

```bash
python -m unittest tests.test_skill_pitch_gate_contracts -v
```

- [ ] **Step 3: Update `production-standard.md`**

Increment version from `2.1` to `2.2`. Add a pitch-review subsection before teacher-sheet production and add blocking failures:

```text
- missing, malformed, non-PASS, or stale level pitch approval;
- PASS record whose passage hash differs from final text;
- missing/non-PASS/stale progression-parity approval;
- fourth unsuccessful patch cycle without fresh redraft;
- reviewer attempt to change teacher-assigned placement;
```

State that semantic approval is agent-owned, while hash/current-state validity is mechanically checked.

- [ ] **Step 4: Update `powerpoint-pack-contract.md`**

Add to the working source record for each group:

```json
{
  "passage_sha256": "...",
  "revision_cycle": 1,
  "pitch_review": {"reviewer_role": "alpha-pitch-reviewer", "verdict": "PASS", "passage_sha256": "..."}
}
```

Add one set-level `progression_review` containing all five hashes. Require `pitch-review-audit.json` from `scripts/validate_pitch_review_package.py` before layout/release. Keep this separate from the existing `layout manifest` and `audit_reading_pack.py`.

- [ ] **Step 5: Run contract tests and confirm GREEN**

```bash
python -m unittest tests.test_skill_pitch_gate_contracts -v
```

- [ ] **Step 6: Commit Task 5**

```bash
git add references/production-standard.md references/powerpoint-pack-contract.md tests/test_skill_pitch_gate_contracts.py
git commit -m "feat: make pitch approvals release-blocking evidence"
```

---

### Task 6: Add persistent adversarial agent scenarios and run behavioural validation

**Files:**
- Create: `tests/fixtures/pitch-agent-cases.json`
- Create: `docs/validation/level-pitch-agent-validation.md`

**Interfaces:**
- Each fixture supplies: `case_id`, `assigned_role`, weekly context, candidate passage, visual plan, provisional question intent, and `expected_verdict`/required issue category.
- Behavioural validation uses a fresh isolated agent context for each case and the exact role file under test.

- [ ] **Step 1: Create the fixture set before tuning role prompts further**

Include all fourteen spec cases. At minimum encode these exact expectations:

```json
[
  {"case_id":"alpha-childish", "assigned_role":"alpha-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"age_appropriateness"},
  {"case_id":"alpha-dense-syntax", "assigned_role":"alpha-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"syntax"},
  {"case_id":"beta-vocab-only", "assigned_role":"beta-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"vocabulary_morphology"},
  {"case_id":"gamma-underpitched", "assigned_role":"gamma-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"response_demand"},
  {"case_id":"delta-length-only", "assigned_role":"delta-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"inference_ambiguity"},
  {"case_id":"epsilon-long-year5", "assigned_role":"epsilon-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"syntax"},
  {"case_id":"epsilon-topic-drift", "assigned_role":"epsilon-pitch-reviewer", "expected_verdict":["REVISE","REJECT"], "must_flag":"age_appropriateness"}
]
```

Also include one correctly pitched case for each level and two set-level parity cases: Beta/Gamma near-duplication and conceptual content removed from Alpha.

- [ ] **Step 2: Run each case against a fresh reviewer context**

Use the runtime's independent subagent mechanism. Provide only the role file, relevant profile definitions, and that case's input contract. Do not leak expected verdicts to the reviewer.

For each result, verify:
- output parses as JSON;
- assigned group/role is correct;
- hash matches the exact candidate;
- verdict is within expected set;
- required issue category is identified;
- reviewer does not propose placement changes.

- [ ] **Step 3: Record the first behavioural run**

In `docs/validation/level-pitch-agent-validation.md`, create a table:

```text
Case | Role | Expected | Actual | Contract valid? | Key finding | Pass?
```

Do not alter expected outcomes after seeing results.

- [ ] **Step 4: Refine role wording only for observed failures, then rerun failed cases**

Follow skill-writing TDD: capture the exact reviewer rationalisation or omission, amend the smallest relevant role instruction, rerun the failed case in a fresh context, and record both attempts.

- [ ] **Step 5: Run all deterministic tests**

```bash
python -m unittest discover -s tests -v
```

Expected: zero failures.

- [ ] **Step 6: Commit Task 6**

```bash
git add tests/fixtures/pitch-agent-cases.json docs/validation/level-pitch-agent-validation.md agents/roles
git commit -m "test: validate pitch agents against adversarial cases"
```

---

### Task 7: Forward-test the recent Term 3 Week 9 failure upstream

**Files:**
- Modify: `docs/validation/level-pitch-agent-validation.md`
- Temporary working files only: `work/term3-week9-forward-test/` (ignored by `.gitignore`).

**Interfaces:**
- Blueprint is fixed for this forward test:
  - Term 3 Week 9
  - Reading Focus: `Reliability and credibility`
  - Learning Intention: `Evaluate whether information deserves confidence.`
  - Success Criteria: `I can use authorship, evidence, purpose and consistency to make a supported judgement about reliability.`
- The test must demonstrate the previously observed Alpha over-explicitness and Epsilon under-pitch are blocked before layout.

- [ ] **Step 1: Create a clean forward-test blueprint and first-pass five-text set**

Use the same age-appropriate community/emergency-information context as the previous pack, but stop before PowerPoint layout. Include provisional question-intent targets only.

- [ ] **Step 2: Intentionally reproduce the two known defects in a controlled baseline**

Baseline Alpha must include an explicit answer-giveaway sentence equivalent in function to “this source is trustworthy because it is current, official and specific”. Baseline Epsilon must be a longer but otherwise ordinary Year 5-style passage with predominantly local evidence.

These are test fixtures, not final teaching text.

- [ ] **Step 3: Dispatch all five level reviewers**

Expected:
- Alpha: `REVISE` or `REJECT`, flagging `explicitness/evidence_distance` because the target judgement is handed to students.
- Epsilon: `REVISE` or `REJECT`, flagging syntax/cohesion/evidence-distance/ambiguity because length alone does not create Year 9 reading complexity.
- Other groups: verdicts according to their actual pitch; do not force a pass.

- [ ] **Step 4: Revise through the central writer and re-review the same affected levels**

Do not bypass the original reviewer. Recompute hashes after every change. Continue only when all five have valid current `PASS` records within the three-cycle limit.

- [ ] **Step 5: Run progression/parity review**

Require `PASS` for the exact five current hashes. If it returns `REVISE_LEVELS`, revise only specified levels, re-run their individual review(s), then re-run parity.

- [ ] **Step 6: Build and validate the pitch-review package mechanically**

Run:

```bash
python scripts/validate_pitch_review_package.py \
  --package work/term3-week9-forward-test/pitch-review-package.json \
  --out work/term3-week9-forward-test/pitch-review-audit.json
```

Expected: `status: PASS`, exit `0`.

- [ ] **Step 7: Finalise question records only after pitch approval**

Apply `references/naplan-reading-question-design.md` to the approved passages. Confirm any subsequent passage edit invalidates the pitch package and forces re-review.

- [ ] **Step 8: Record forward-test evidence**

Add to `docs/validation/level-pitch-agent-validation.md`:
- which initial defects were caught;
- revision counts per group;
- final level verdicts/hashes;
- parity verdict;
- mechanical validator result;
- confirmation that no layout was attempted before pitch approval.

- [ ] **Step 9: Run complete deterministic test suite**

```bash
python -m unittest discover -s tests -v
```

Then run the existing audit script's help/import smoke check to ensure no regression to the existing tool:

```bash
python scripts/audit_reading_pack.py --help
```

Expected: exit `0`.

- [ ] **Step 10: Commit Task 7**

```bash
git add docs/validation/level-pitch-agent-validation.md
git commit -m "test: forward validate level pitch agent workflow"
```

---

### Task 8: Final integration review and release candidate PR

**Files:**
- Review all feature files; no new feature scope.

**Interfaces:**
- Release candidate is the branch diff against `main`.

- [ ] **Step 1: Run all tests fresh**

```bash
python -m unittest discover -s tests -v
python scripts/audit_reading_pack.py --help
```

Expected: zero unittest failures; audit script help exits `0`.

- [ ] **Step 2: Validate a known-good pitch review package fresh**

```bash
python scripts/validate_pitch_review_package.py \
  --package work/term3-week9-forward-test/pitch-review-package.json \
  --out work/term3-week9-forward-test/pitch-review-audit-final.json
```

Expected: `PASS`, exit `0`.

- [ ] **Step 3: Diff review against the approved spec**

Check every spec success criterion explicitly:
- five independent reviewer roles exist;
- writer cannot self-approve;
- reviewer information barriers are documented;
- exact-hash binding works;
- stale approvals fail;
- three-cycle limit fails closed;
- parity gate is set-hash bound;
- placements/40-week sequence are unchanged;
- question/layout stages occur only after pitch approval;
- forward test caught Alpha over-explicitness and Epsilon under-pitch.

- [ ] **Step 4: Verify no unintended edits**

Confirm `references/40-week-reading-overview.md`, `references/group-profiles.md`, `references/naplan-reading-question-design.md`, and `scripts/audit_reading_pack.py` are unchanged unless a separately justified fix was required and reviewed.

- [ ] **Step 5: Open a PR from the implementation branch to `main`**

PR body must list deterministic tests, behavioural agent cases, Term 3 Week 9 forward-test result, and explicit non-goals. Do not merge until those results have been independently checked.
