# Level-Pitch Agent Orchestration

This contract governs the weekly passage-pitch workflow. It is runtime-neutral: use independent agent dispatch when available; otherwise use isolated sequential role invocations without collapsing writer and reviewer into one self-approving pass.

## Required order

1. Resolve the **weekly blueprint**: Reading Focus, Learning Intention, Success Criteria, curriculum context, conceptual spine, verified facts, visual constraints and provisional question-intent targets.
2. The **central passage writer** drafts Alpha-Epsilon from the same blueprint.
3. Compute exact **SHA-256** for each candidate passage.
4. Dispatch the **five level reviewers** independently. Parallel preferred. Each receives only its assigned candidate passage, profile definitions and approved context.
5. Validate each reviewer record before accepting its verdict.
6. Send only required revisions plus the original blueprint back to the writer. The same level reviewer rechecks the revised passage.
7. Re-hash every wording change; mark prior level and parity approvals as **stale approvals** and invalidate dependent question records where evidence or answerability changed.
8. Continue for at most **three revision cycles** per passage. A fourth unsuccessful attempt requires a fresh redraft from the blueprint.
9. After five current `PASS` records, dispatch the **progression/parity** reviewer with all five exact passages and hashes.
10. Accept progression/parity `PASS` only when its five hashes match the current passage set.
11. Only then begin **final question writing** and question/evidence QA.
12. Any later passage edit returns the affected level to pitch review and then repeats progression/parity review.
13. Only current approved passages and valid question records proceed to **PowerPoint layout**.

## Reviewer isolation

Level reviewers do not see neighbouring candidate passages, other level-review verdicts or the writer's self-assessment. They may consult the authoritative profile definitions for boundary reference. Only the progression/parity reviewer sees all five approved passages together.

## Parallel and sequential execution

**Parallel preferred:** dispatch Alpha-Epsilon reviewers independently at the same time where the runtime supports it.

**Sequential fallback:** call each reviewer separately and clear prior reviewer output from the next review context. Do not provide neighbouring candidate passages or prior verdicts. The same schemas, SHA-256 binding, revision-cycle rules and release gates apply.

## Fail-closed review records

Every level review conforms to `agents/schemas/pitch-review.schema.json`. The package is mechanically validated by:

```text
python scripts/validate_pitch_review_package.py --package <pitch-review-package.json> --out <pitch-review-audit.json>
```

A package cannot pass with missing reviews, stale hashes, non-PASS verdicts, revision cycles above three, placement-change fields or a stale progression review.

Teacher override is possible only through explicit teacher direction recorded in the working source record. Record the gate overridden and why; do not silently convert a failed review into a pass.
