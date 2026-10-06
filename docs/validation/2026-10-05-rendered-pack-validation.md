# Controlled rendered-pack validation

Status: **PASS within the recorded cloud-rendered sample scope; not a production release**

The approved fictional Term 3 Week 9 bridge/fair passages and 15 final questions produced an editable Guided print deck with 131 exact-A4-landscape sheets: one teacher sheet per group and seven complete student copies. A separate fictional seed-swap Shared deck contains eight 16:9 slides, alternating one paragraph/question with its matched answer.

All 139 slides were individually opened and inspected at full original detail. Final v5 image hashes bind every review to the delivered artifacts. Alpha/Beta reviews carry forward only where their earlier reviewed PNGs are byte-identical to final v5; all other groups and Shared were inspected on v5. No slide was inferred to pass merely because it duplicated another copy.

The final structural audit is PASS with no warnings, and semantic text reconstruction, editability/package and overflow checks passed. Real renders exposed source-card overlap, teacher-answer overflow, Shared panel-fit issues and detached Delta headings; those were repaired before final approval, without changing approved Guided wording. Teacher and Shared semantic content also passed independent review.

[Per-slide hashes, coverage and recorded checks](2026-10-05-rendered-pack-evidence.json) are retained. The editable decks and complete 18,575,425-byte evidence archive were delivered separately. Artifact identity:

| Artifact | SHA-256 |
| --- | --- |
| Guided_Reading_Print_T3_W9.pptx | `7a4368ebdb21ce0e62ad73538e0fcf50734696d18566da0ef6347f7bc687053a` |
| Shared_Reading_T3_W9.pptx | `eb35019a28be80bce708d0e825383e595f32924d69b937a9244c78ae3671d0a2` |
| Controlled_T3W9_Reading_Validation_Candidate_v5.zip | `62142313ddd2e52cbd77bba7f7f3ac5da40e2960db0b596615f5371d1d45a5a4` |

## Limits

- These are controlled samples, not a verified current-week classroom pack
- The cloud artifact-tool renderer was used; actual PowerPoint opening/editing, repair warnings, screen-reader order and physical/PowerPoint print preview remain unverified
- Guided uses Liberation Sans. Shared retains the verified exemplar's Trebuchet MS declaration, but the recorded renderer lacked that font and did not identify its fallback family; exact Trebuchet/PowerPoint appearance remains unverified
- All scenario people, sources, quantities and events are fictional; no pupil personal data is included
- No installation, scheduling, merge or DLP umbrella integration occurred

This is a post-Week-6 controlled sample. The separate V2 behavioural corpus uses different library-book-swap passages and must not be conflated with these rendered artifacts. The existing integration contract still requires a Weeks 1–6 forward pack and real-host/staging/rollback checks before integration.
