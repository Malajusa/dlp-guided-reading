# Guided Reading validation status

Status: **reviewer subsystem and controlled rendered sample validated within the scopes below; draft, unmerged and uninstalled**

Updated 6 October 2026. The current complete deterministic suite passes **42/42**. A narrow schema follow-up to published commit `87904cfe7f88e23e82e6cbaccbe2cdca38806d50` makes PASS records require empty blockers and revisions, matching the unchanged fail-closed production validator. The earlier three-file authoring/schema-test reconciliation remains the preserved 38-test checkpoint.

## Evidence layers

| Layer | Actual result | Scope |
| --- | --- | --- |
| Original source baseline `6239dcf` | 18/20 | Two pre-existing documentation-contract mismatches were reproduced |
| First repaired checkpoint | 20/20, then 28/28 | Contract repairs and eight validator regressions |
| Published follow-up `5e52b3c` | 32/32 | Role/group schema binding and explicit no-override-bypass coverage |
| Published reconciliation `87904cf` | 38/38 | Explicit both-deck authoring workflow and persistent checks for all three schemas |
| Current PASS-schema follow-up | **42/42** | Four regressions and verdict-dependent empty-blocker/revision constraints |
| Frozen v1 behavioural corpus | 7 expected catches; 5 positive mismatches; 2 invalid-prerequisite parity cases | Historical outcomes remain unchanged |
| Separately frozen v2.0.1 core cases | **12/12 expected outcomes** | Five complete new positives pass; seven unchanged negative cases are caught |
| V2 positive parity | **PASS** | Five real current individual approvals preceded set review; production gate PASS |
| V2 duplicate challenge | **REVISE_LEVELS, as expected** | Identical Beta/Gamma passages earned real separate approvals, then failed set progression; production gate FAIL |
| V2 Alpha content-loss precondition | **REJECT upstream** | Parity was not dispatched; no semantic parity result is claimed |
| Controlled T3W9 rendered sample | **139/139 slides visually inspected** | 131 Guided and 8 Shared slides; semantic, structural, editability/package and overflow checks pass in the recorded cloud renderer |
| Actual PowerPoint/printer host and integration | **Not verified / not performed** | No production installation or classroom scheduling claim |

Local/workspace test results are not hosted CI results. The previously observed GitHub Actions checks were Copilot code review. Their completion must not be presented as execution of the deterministic suite; check the exact current commit's hosted checks separately.

## Current code and contract changes

- Production references consistently retain the three-revision-cycle limit and the structured `progression_review` record
- The validator rejects unexpected reviewer fields, non-string list entries and malformed verdict types; malformed CLI inputs produce a structured FAIL audit
- The level schema encodes exactly the five valid role/group pairs
- Teacher override requests may be recorded, but the current validator has no override input and the request does not waive current level/parity PASS requirements
- Writer authority remains authorship-only; its grammar was clarified without granting self-approval
- Both decks now explicitly follow the installed Presentations skill's current required workflow, speaker-note provenance, rendering, overflow checks and every-slide inspection

The last item is an entrypoint/scope clarification. Those authoring requirements already survived through mandatory references; no effective workflow bypass was demonstrated. The surviving workflow sentence sat under Guided print geometry, so stating both-deck scope directly avoids ambiguity.

The 38-test reconciliation changed only `SKILL.md`, `tests/test_skill_pitch_gate_contracts.py` and the new `tests/test_published_schema_contracts.py`. Runtime validators, schema definitions, profile assignments, reviewer authority, original fixtures and sample content were unchanged by that reconciliation. Persistent tests cover all three meta-schemas plus representative valid/invalid progression and orchestration records. Deliberate schema weakening/malformation checks showed those tests detect the intended defects. The production validator remains standard-library-only; `jsonschema` is a declared test-only dependency.

[38-test patch and test evidence](2026-10-06-patch-validation.json) records that checkpoint's exact source identities and test log. The earlier [hosted-review follow-up](2026-10-05-hosted-review-followup.md) remains a 32-test historical checkpoint, not the current headline.

### PASS-schema consistency follow-up

Two subsequent review findings were reproduced: both review schemas accepted PASS records containing unresolved blockers or required revisions although the production gate rejected them. Four new regression methods failed against `87904cf` before the fix (five failing subcases, including a progression revision map containing `{"Alpha": []}`). The schemas now require empty blocker arrays and empty revision arrays/maps only when the verdict is PASS. Non-PASS revision/rejection records retain their existing schema validity and still cannot release a package.

The complete suite passes 42 tests, including all three meta-schema checks. Recorded V2 replay validates all 15 standalone level reviews, both set reviews and their 10 embedded level reviews against the updated schemas. The positive set still produces production PASS and the duplicate set produces FAIL. The original forward package remains PASS; its stale-Epsilon mutation remains FAIL. Production validator bytes, reviewer content, frozen fixtures and all recorded evidence are unchanged. These are deterministic checks and retained-record replays; no new model run or slide render is claimed.

## Preserved behavioural history

The original fourteen-case fixture and [its complete recorded evidence](2026-10-05-level-pitch-evidence.json) remain byte-for-byte unchanged. The five short prescribed positives were returned for revision because their inputs did not supply sufficient evidence, purpose or independent synthesis demands. The original parity cases contained placeholders and lacked five current individual PASS prerequisites. Those findings have not been relabelled as successes.

The separately versioned v2.0.1 corpus froze new candidate bytes, expected outcomes and diagnostic targets before execution. It uses a different fictional library-book-swap scenario. Fifteen fresh level contexts and two fresh set contexts produced the recorded outcomes above without revising a fixture or weakening profiles during the run.

[V2 results](2026-10-05-v2-behavioural-results.md) and [detailed V2 input/output evidence](2026-10-05-v2-behavioural-evidence.json) preserve actual reviews, hashes and real-record set packages. The duplicate challenge reached a legitimate semantic review only after its prerequisites genuinely passed. The Alpha-loss path demonstrates upstream blocking only.

Isolation claims are limited to fresh contexts and controller-supplied inputs. Full provider tool history and filesystem-enforced confinement were unavailable. Worker access statements are attributed self-reports. No provider logs, favourable approvals or strict-receipt-wrapper success were fabricated. Some declared SVGs were inspected as source without rendering, so these pitch reviews do not establish final print scale.

## Controlled forward test and rendered pack

The original controlled T3W9 bridge/fair forward test caught Alpha's answer giveaway and Epsilon's length-without-complexity defect. The central writer revised those two passages once; their same assigned reviewers then passed them. Beta, Gamma and Delta passed initially and stayed byte-identical. A new set reviewer passed the current five-text package, and the production validator passed it. A later Epsilon wording mutation correctly failed its current, individual-review and set-review hashes.

Only after current pitch/parity approval were the fifteen question records finalised and independently checked. The resulting [controlled rendered-pack report](2026-10-05-rendered-pack-validation.md) and [per-slide evidence](2026-10-05-rendered-pack-evidence.json) cover all 139 final images. Real rendering found and repaired overlaps, overflow, panel-fit problems and orphaned headings without changing approved Guided wording. Do not confuse this rendered bridge pack with the separate V2 library passages.

Shared retains the verified exemplar's Trebuchet MS declaration, but the recorded cloud renderer lacked that font and did not report its fallback family. Exact Trebuchet/PowerPoint appearance remains unverified. All scenarios are fictional; no pupil personal data is included.

## Reproduce the deterministic and recorded-package checks

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The committed data permits mechanical replay of the two V2 set packages:

```sh
python - <<'PY'
import json
from pathlib import Path
from scripts.validate_pitch_review_package import validate_review_package
record = json.loads(Path('docs/validation/2026-10-05-v2-behavioural-evidence.json').read_text())
expected = {'s-726c': 'PASS', 's-5a10': 'FAIL'}
for case in record['set_tests']:
    audit = validate_review_package(case['package'])
    assert audit['status'] == expected[case['trial_id']]
    print(case['trial_id'], case['review']['verdict'], audit['status'])
PY
```

This replays retained records. It neither dispatches fresh model reviewers nor converts subjective reading-pitch judgements into empirical classroom or readability measurements.

## Remaining release boundary

Keep the PR draft. Do not merge, install, deploy, schedule or describe it as production-authoritative on this evidence alone.

- Verify actual PowerPoint opening/editing, repair warnings, font behaviour, screen-reader order and physical/PowerPoint print preview
- Resolve current teaching dates, timetable and assessment inputs before producing a current-week classroom pack
- Complete a Weeks 1–6 curriculum-aligned forward pack in addition to the post-Week-6 sample
- Follow the existing staged integration, dependency-closure and rollback contract before any explicitly approved DLP integration

The installed timetable-only Guided Reading boundary remains untouched. The inherited extreme-malformed-nesting limitation for direct Python callers remains disclosed; the documented CLI returns a FAIL audit for that case.
