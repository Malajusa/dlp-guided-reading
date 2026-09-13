---
name: dlp-guided-reading
description: Generate and quality-assure next-week Shared Reading and differentiated Alpha-Epsilon Guided Reading PowerPoint packs for a WA Year 4/5 class within the Daily Lesson Pack. Use for weekly reading-pack planning or production; do not assess students, change teacher placements, or generate a generic daily reading passage.
---

# Weekly Shared and Guided Reading Pack

Create the following teaching week's coordinated reading pack. Reading instruction is the priority; HASS, Health, and Design and Technologies supply worthwhile knowledge and contexts.

Read the references required by the task:

- Always read [the production standard](references/production-standard.md).
- Always read [the 40-week reading overview](references/40-week-reading-overview.md) to resolve the prescribed Reading Focus, Learning Intention, and Success Criteria.
- Always read [the NAPLAN-informed question design standard](references/naplan-reading-question-design.md) before writing or revising comprehension questions.
- Always read [the agent orchestration contract](references/agent-orchestration.md) before drafting Guided Reading passages.
- Read [the curriculum map](references/curriculum-map.md) when selecting or checking a weekly topic, genre, or curriculum alignment.
- Read [the group profiles](references/group-profiles.md) before writing or reviewing Alpha-Epsilon texts.
- Read [the PowerPoint pack contract](references/powerpoint-pack-contract.md) before creating, revising, or auditing files.
- Read [the Daily Lesson Pack integration contract](references/daily-lesson-pack-integration.md) only when packaging, installing, or changing umbrella routing.

## Resolve the week

Resolve target dates, term, week, interruptions, current plan and assessment priorities from authoritative sources. Source order:

1. current teacher instruction;
2. explicit lesson-status or assessment updates;
3. authoritative timetable/calendar;
4. 40-week reading overview;
5. detailed weekly plans;
6. whole-year curriculum plan/curriculum map;
7. standing defaults.

The 40-week overview is the default instructional sequence. Assessment evidence may refine emphasis, modelling, scaffolding, evidence distance, question design and group next steps, but does not silently replace the prescribed weekly focus.

## Build one coordinated weekly blueprint

Before drafting, establish:

- prescribed Reading Focus, Learning Intention and Success Criteria;
- previously taught comprehension processes to spiral;
- curriculum source/topic and verified facts;
- current Writing genre/features during Weeks 1-6;
- Shared Reading comprehension model;
- common Guided Reading conceptual spine;
- provisional question-intent targets: reasoning, evidence distance and response depth;
- group-specific access controls and visual plans;
- cultural and safety constraints.

Shared and Guided Reading use distinct passages. Guided Reading provides five genuine rewrites of one common conceptual spine.

## Gate passage pitch before final questions

Full weekly generation must follow `references/agent-orchestration.md`:

1. the central passage writer drafts all five passages;
2. five independent level reviewers assess Alpha, Beta, Gamma, Delta and Epsilon against their authoritative profiles;
3. revise through the central writer until there are **five current level PASS** records bound to the exact passage hashes, within the three-cycle limit;
4. run the progression/parity reviewer and obtain a current **progression/parity PASS** bound to all five hashes;
5. only then finalise question records and proceed **before PowerPoint layout**.

Any wording change makes the affected level approval stale and invalidates parity approval. If the passage change affects answerability or evidence locations, dependent question records are also stale.

Parallel reviewer dispatch is preferred. If the runtime cannot dispatch independent agents, use the development sequential fallback defined in the orchestration contract: invoke each reviewer role in isolation, do not expose neighbouring candidate passages or prior verdicts, and retain the same fail-closed review records. Never allow the passage writer to self-approve.

## Design questions deliberately

Apply the NAPLAN-informed question design standard to every substantive question. Design intended reasoning and evidence demand before polishing wording. Text complexity and question complexity are separate controls.

Use multiple choice only when discrimination between plausible interpretations has instructional value. Record why each distractor is plausible but wrong. For constructed responses distinguish answer, acceptable evidence and reasoning link where needed.

Generate teacher guidance, questions and answers from the same source record as the approved final passages. Any passage revision invalidates dependent question records until rechecked.

## Preserve teacher-assigned groups

Fixed rotation:

- Monday: Alpha
- Tuesday: Beta
- Wednesday: Gamma
- Thursday: Delta
- Friday: Epsilon

Teacher assessment is authoritative. Do not reassess students, change membership, rename groups, infer new placements, or weaken Epsilon. Student-facing material shows only the Greek group name and never assessed profile/difficulty labels.

## Create PowerPoint outputs

Produce one Shared Reading projection deck and one editable Guided Reading print deck containing all five teacher sheets and seven complete student copies per group. Use exact A4 landscape for the print deck. Keep instructional text editable and visuals separate.

Printing one copy of the complete guided deck must yield one teacher sheet and seven complete student sets per scheduled group.

## Verify and release

Before layout/release, require a current `PASS` from `scripts/validate_pitch_review_package.py`. Then maintain the layout manifest and run:

```text
python scripts/audit_reading_pack.py --manifest <manifest.json> --guided-deck <guided.pptx> --shared-deck <shared.pptx> --out <audit.json>
```

Render and inspect every slide at full size. Structural success does not override weak differentiation, stale pitch approval, factual/cultural issues, unsupported inference, weak distractors, unreadable pages or unhelpful visuals.

## Boundaries

- A missed group remains `not taught` until the teacher reschedules it.
- Relief packs omit Guided Reading unless explicitly requested.
- Morning Work, Literacy Warm-up, Shared Reading, Guided Reading and independent reading use different passages.
- Weekly production is not permission to create a scheduler.
- Supplied Technologies coverage is Design and Technologies, not Digital Technologies.
- NAPLAN materials inform question construction only; do not turn Guided Reading into standardised-test rehearsal.
