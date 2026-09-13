# Level-Pitch Agent Validation

Status: **implementation candidate; behavioural agent gate pending**

Date: 2026-09-13

## Deterministic validation

The implementation was exercised locally against the planned unittest suite.

- `tests/test_validate_pitch_review_package.py`: 13 tests passed.
- `tests/test_agent_role_contracts.py`: 3 tests passed.
- `tests/test_skill_pitch_gate_contracts.py`: 4 tests passed.
- Full `python -m unittest discover -s tests -v`: **20 tests, 0 failures**.

The validator covers missing reviews, stale passage hashes, stale set-level hashes, non-PASS verdicts, malformed dimensions, revision cycles above three, placement-change fields, and PASS records that still contain blocking/revision requirements.

## Adversarial behavioural cases

Expected outcomes are fixed in `tests/fixtures/pitch-agent-cases.json` and must not be changed after seeing reviewer outputs.

| Case | Role | Expected | Actual | Contract valid? | Key finding | Pass? |
| --- | --- | --- | --- | --- | --- | --- |
| alpha-childish | Alpha | REVISE/REJECT | NOT RUN | — | age appropriateness | PENDING |
| alpha-dense-syntax | Alpha | REVISE/REJECT | NOT RUN | — | syntax | PENDING |
| beta-vocab-only | Beta | REVISE/REJECT | NOT RUN | — | vocabulary/morphology-only difficulty | PENDING |
| gamma-underpitched | Gamma | REVISE/REJECT | NOT RUN | — | insufficient independent response demand | PENDING |
| delta-length-only | Delta | REVISE/REJECT | NOT RUN | — | insufficient inference/ambiguity progression | PENDING |
| epsilon-long-year5 | Epsilon | REVISE/REJECT | NOT RUN | — | insufficient syntactic/reading complexity | PENDING |
| epsilon-topic-drift | Epsilon | REVISE/REJECT | NOT RUN | — | topic drift / age appropriateness | PENDING |
| alpha-well-pitched | Alpha | PASS | NOT RUN | — | positive boundary case | PENDING |
| beta-well-pitched | Beta | PASS | NOT RUN | — | positive boundary case | PENDING |
| gamma-well-pitched | Gamma | PASS | NOT RUN | — | positive boundary case | PENDING |
| delta-well-pitched | Delta | PASS | NOT RUN | — | positive boundary case | PENDING |
| epsilon-well-pitched | Epsilon | PASS | NOT RUN | — | positive boundary case | PENDING |
| parity-beta-gamma-duplicate | Progression/parity | REVISE_LEVELS/REJECT_SET | NOT RUN | — | adjacent-group duplication | PENDING |
| parity-alpha-content-loss | Progression/parity | REVISE_LEVELS/REJECT_SET | NOT RUN | — | conceptual content loss | PENDING |

**Reason not run:** the current ChatGPT connector session does not expose a fresh subagent/agent-dispatch mechanism. Running these cases through the controller itself would not meet the approved independence requirement. No behavioural passes are claimed.

Run this table in Codex or another runtime with independent subagent contexts before merging the feature.

## Term 3 Week 9 mechanical forward test

Blueprint remains:

- Reading Focus: Reliability and credibility
- Learning Intention: Evaluate whether information deserves confidence.
- Success Criteria: I can use authorship, evidence, purpose and consistency to make a supported judgement about reliability.

A controller-authored five-passage package was used only to verify the mechanical approval chain. It is not evidence that the reviewer prompts themselves passed behavioural testing.

Result from `validate_pitch_review_package.py`:

- current five-text package: **PASS**;
- revision cycles: within limit;
- five level hashes: current;
- progression/parity hashes: current.

A negative stale-state test then changed Epsilon after its recorded approval. The validator returned **FAIL / exit 1** and reported all three expected stale-state failures:

1. Epsilon `current_sha256` no longer matched the exact passage text;
2. Epsilon level-review hash was stale;
3. progression/parity Epsilon hash was stale.

This demonstrates that approved text cannot be changed silently before final question writing/layout.

## Known Term 3 Week 9 defects encoded for future behavioural test

The prior manual pack review identified:

- Alpha over-explicitness: the passage could state the reliability judgement instead of leaving students to make it;
- Epsilon under-pitch: greater length without sufficient syntactic, cohesion, evidence-distance or ambiguity demand.

Those defects are represented by `alpha-*` and `epsilon-long-year5` fixtures. They must be caught by fresh independent reviewers before this feature can be marked release-ready.

## Release status

Deterministic implementation: **PASS**.

Independent behavioural review: **PENDING / BLOCKING**.

Do not describe this subsystem as fully validated or production-authoritative until all fourteen behavioural cases and the Term 3 Week 9 fresh-agent forward test have been run and recorded.
