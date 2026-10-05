# Level-Pitch Agent Validation

Status: **implementation and controlled forward workflow pass; legacy behavioural corpus unresolved; draft release candidate**

Validated on 5 October 2026 against PR3 source commit `6239dcfbe0852f794ed28157d005d2ef91dc831b`. The immutable 30-file source snapshot was checked against GitHub blob hashes before work. All original reviewer roles, authoritative profiles, question standard, 40-week overview and 14-case fixtures remain unchanged.

## Evidence summary

| Layer | Result | What it establishes |
| --- | --- | --- |
| Source provenance | Verified | Exact PR3 source, no claim about an installed desktop copy |
| Original deterministic baseline | 18/20 | Two contract tests failed despite the earlier 20/20 report |
| Repaired original suite | 20/20 | Contract terminology and structured parity record repaired without changing tests |
| Final deterministic suite | 28/28, exit 0 | Eight added regression tests cover schema and malformed-input handling |
| Independent schema mutation probe | 752 cases; 656 schema-invalid; zero invalid PASS, zero unexpected exceptions | Targeted record-shape robustness |
| Frozen behavioural corpus | 7 expected catches, 5 positive mismatches, 2 input-contract-blocked parity cases | Actual results below; not an all-pass corpus |
| Fresh T3W9 writer and pitch workflow | PASS | Real isolated review, revision, current-hash binding and parity |
| Final question/evidence QA | PASS | 15 hash-bound questions reviewed against exact approved passages |
| Rendered pack / real desktop host / installation | NOT RUN | No production or classroom release claim |

Full synthetic inputs, raw review outputs, revision history, passage hashes, audits and red/green test logs are retained in [the validation evidence](2026-10-05-level-pitch-evidence.json).

## Implementation repairs

- Both production references now consistently name the existing **three revision cycles** limit.
- The PowerPoint source record explicitly names `progression_review` and its authoritative schema.
- The validator rejects unexpected reviewer properties and non-string list items, rather than accepting schema-invalid PASS records.
- Malformed verdict types return FAIL rather than raising unhashable-type errors.
- CLI parsing and excessive-nesting failures write structured FAIL audit files.
- No new runtime dependencies were introduced; the production validator remains standard-library-only.

The independent patch audit reproduced the six schema failures on the immutable baseline, then verified all eight new regressions and the final suite. Its 752-case mutation probe used the published schemas as an independent oracle. This is targeted evidence, not a proof over every possible input. The inherited extreme-nesting exception for direct Python callers remains a nonblocking limitation; the documented CLI gate is protected.

## Frozen behavioural cases

Every case used a fresh isolated reviewer context with only its exact candidate, approved context, role, profile definitions and output schema. No expected verdict, diagnostic category, descriptive case label, neighbouring passage or prior verdict was supplied. Every output was checked against its JSON schema, role/group identity and exact passage hash. Original fixture expectations were frozen throughout.

| Case | Frozen expected | Actual | Result |
| --- | --- | --- | --- |
| alpha-childish | REVISE/REJECT | REJECT | PASS |
| alpha-dense-syntax | REVISE/REJECT | REJECT | PASS |
| beta-vocab-only | REVISE/REJECT | REJECT | PASS |
| gamma-underpitched | REVISE/REJECT | REVISE | PASS |
| delta-length-only | REVISE/REJECT | REVISE | PASS |
| epsilon-long-year5 | REVISE/REJECT | REVISE | PASS |
| epsilon-topic-drift | REVISE/REJECT | REVISE | PASS |
| alpha-well-pitched | PASS | REVISE | FAIL: expected PASS |
| beta-well-pitched | PASS | REVISE | FAIL: expected PASS |
| gamma-well-pitched | PASS | REVISE | FAIL: expected PASS |
| delta-well-pitched | PASS | REVISE | FAIL: expected PASS |
| epsilon-well-pitched | PASS | REVISE | FAIL: expected PASS |
| parity-beta-gamma-duplicate | REVISE_LEVELS/REJECT_SET | REVISE_LEVELS | BLOCKED: invalid prerequisites |
| parity-alpha-content-loss | REVISE_LEVELS/REJECT_SET | REVISE_LEVELS | BLOCKED: invalid prerequisites |

All seven defect cases identified their required diagnostic category. All five prescribed positive excerpts were returned for revision. Their common shortcomings were missing concrete corroborating evidence or source-purpose information; Gamma–Epsilon also lacked the distributed evidence or independent synthesis required by their profiles. Complete forward-test candidates did pass the unchanged roles, so these results do not demonstrate an indiscriminate reject-all policy.

Both parity cases contain placeholder texts and no current individual PASS records. Their reviewers reported the expected duplication/content-loss observations, but the missing prerequisites prevent counting either as a valid semantic parity pass. No approvals were fabricated.

**Do not relabel this 14-case corpus as passing.** Preserve these results and review a separately versioned, complete positive/parity fixture design before treating a replacement corpus as a release gate. Changing the original expected outcomes after observing these results would invalidate the baseline.

## Controlled Term 3 Week 9 forward test

- Reading Focus: Reliability and credibility
- Learning Intention: Evaluate whether information deserves confidence.
- Success Criteria: I can use authorship, evidence, purpose and consistency to make a supported judgement about reliability.
- Context: a fully fictional community fair and competing bridge-access messages; no classroom personal data or real emergency advice.

A central writer created all five complete candidates. The controlled initial Alpha supplied its intended reliability judgement, while initial Epsilon used lengthy ordinary prose with local, explicit conclusions. Reviewers were blind to these injected defects.

| Group | Initial verdict | Revision count | Final verdict |
| --- | --- | --- | --- |
| Alpha | REVISE: answer giveaway | 1 | PASS |
| Beta | PASS | 0 | PASS |
| Gamma | PASS | 0 | PASS |
| Delta | PASS | 0 | PASS |
| Epsilon | REVISE: under-pitch and supplied synthesis | 1 | PASS |

The central writer repaired only Alpha and Epsilon. Beta, Gamma and Delta remained byte-for-byte unchanged. The same assigned level reviewers rechecked their revised passages. Only after five schema-valid current individual PASS records did a new progression/parity reviewer receive the complete set; it returned PASS with all five exact hashes. No teacher override was used.

| Group | Revision cycle | Final passage SHA-256 |
| --- | --- | --- |
| Alpha | 1 | `8c2762847aeeb91ffe2d01b2decb7366e6e1fa64eb378148fd542b8977c8d082` |
| Beta | 0 | `7e513c29075f264696bf1c705930117f73220acb38c87bdc0c2c1310257e24dc` |
| Gamma | 0 | `61b187548b3588f93c906ad12f9d49e7c9329ed174874c05a028c3eb62298805` |
| Delta | 0 | `12bcbed047f2ae28f9c6d00b635fd2f21b656bf8ccffcd45c7f33a18e907aa29` |
| Epsilon | 1 | `1003f4875b2501b1be354a969e5f370f6636cc8a51d684405e17db3ce8294056` |

The final pitch-review package returns **PASS / exit 0**. A separate negative test appends wording to approved Epsilon while retaining its recorded hashes and returns **FAIL / exit 1**, identifying all three stale states: current passage hash, Epsilon level-review hash and progression/parity hash.

Only after that gate passed were 15 final question records written. They are hash-bound to the approved text and independently checked for answerability, evidence location/distance, scaffold neutrality, uncertainty, group progression and student-facing Greek labels. No passage wording changed during question writing or QA. No layout was created before approval.

## Release boundary and next steps

This is evidence for the reviewer subsystem in the cloud validation environment. It does not establish a rendered PowerPoint release, a real desktop-host invocation, installation or Daily Lesson Pack integration. The installed timetable-only Guided Reading boundary remains untouched.

1. Resolve the frozen positive/parity corpus deficiencies in a separately versioned fixture design; retain this baseline and predeclare replacement expectations before a fresh run.
2. Complete the standalone rendered-pack and real-host tests, including editable text, full-size slide inspection, copy counts, visual restrictions and teacher/student parity.
3. Before any umbrella integration, satisfy the existing integration contract, including both Weeks 1–6 and post-Week-6 pack tests, staged replacement, dependency closure and rollback.

Keep PR3 draft. Do not merge, install or describe the component as production-authoritative on this evidence alone.
