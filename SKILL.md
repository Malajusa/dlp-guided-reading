---
name: dlp-guided-reading
description: Generate and quality-assure next-week Shared Reading and differentiated Alpha-Epsilon Guided Reading PowerPoint packs for a WA Year 4/5 class within the Daily Lesson Pack. Use for weekly reading-pack planning or production; do not assess students, change teacher placements, or generate a generic daily reading passage.
---

# Weekly Shared and Guided Reading Pack

Create the following teaching week's coordinated reading pack. Reading instruction is the priority; HASS, Health, and Design and Technologies supply worthwhile knowledge and contexts.

Read the references required by the task:

- Always read [the production standard](references/production-standard.md).
- Always read [the 40-week reading overview](references/40-week-reading-overview.md) to resolve the prescribed Reading Focus, Learning Intention, and Success Criteria for the target term and week.
- Always read [the NAPLAN-informed question design standard](references/naplan-reading-question-design.md) before writing or revising comprehension questions.
- Read [the curriculum map](references/curriculum-map.md) when selecting or checking a weekly topic, genre, or curriculum alignment.
- Read [the group profiles](references/group-profiles.md) before writing any Alpha-Epsilon text or teacher guidance.
- Read [the PowerPoint pack contract](references/powerpoint-pack-contract.md) before creating, revising, or auditing files.
- Read [the Daily Lesson Pack integration contract](references/daily-lesson-pack-integration.md) only when packaging, installing, or changing umbrella routing.

## Resolve the week

The normal production run occurs on Monday morning for the following teaching week. Resolve the target dates, term, week, school interruptions, current plan, and any recorded assessment priorities from authoritative local sources. Do not treat the computer date alone as proof of the teaching week.

Use this source order:

1. the user's current instruction;
2. explicit lesson-status or assessment updates;
3. the authoritative timetable and calendar;
4. [the 40-week reading overview](references/40-week-reading-overview.md) for the prescribed Reading Focus, Learning Intention, and Success Criteria;
5. detailed weekly plans;
6. the whole-year curriculum plan and [curriculum map](references/curriculum-map.md);
7. standing defaults in this skill.

The 40-week overview is the default instructional sequence. Do not silently replace its prescribed weekly reading focus because a different comprehension strategy, curriculum topic, or assessment priority appears convenient. Teacher assessment may refine emphasis, modelling, scaffolding, evidence distance, question design, or group-specific next steps. Change the overview sequence only when the teacher explicitly directs that change.

For Weeks 1-6, select a suitable curriculum subtopic and Writing connection that serve the prescribed reading focus. After Week 6, use assessment evidence to sharpen the prescribed focus and choose the most useful text form or context; use curriculum-area balance only as a tie-breaker when multiple contexts serve the same reading need.

## Build one coordinated weekly sequence

Establish one weekly blueprint before drafting:

- prescribed Reading Focus, Learning Intention, and Success Criteria from the 40-week overview;
- previously taught comprehension processes that should spiral into the week's reading;
- curriculum source area and precise topic;
- essential facts, concepts, vocabulary, and source evidence;
- current Writing genre and useful features during Weeks 1-6;
- whole-class comprehension model for Shared Reading;
- common conceptual spine for Guided Reading;
- group-specific reading targets and access controls;
- intended evidence distance and response depth;
- a structured question plan identifying target reasoning, evidence location/distance, expected answer, and acceptable evidence for each substantive question;
- visual purposes and cultural or safety constraints.

Previously taught comprehension processes remain available throughout the year. The nominated weekly Reading Focus controls explicit teaching emphasis; it does not prohibit mixed literal, inferential, vocabulary, synthesis, or evaluative questions where appropriate. Increase evidence distance and independence across the year in line with the 40-week overview.

Shared and Guided Reading must use distinct passages. They may share the topic, genre, knowledge, and selected vocabulary. Shared Reading explicitly models a useful meaning-making move; Guided Reading provides five genuine rewrites through which students apply or extend the learning at the teacher-assigned level.

## Design questions deliberately

Apply [the NAPLAN-informed question design standard](references/naplan-reading-question-design.md) to every substantive comprehension question. Design the intended reasoning and evidence demand before polishing the wording. Treat text complexity and question complexity as separate controls.

Use multiple choice only when discriminating between plausible interpretations has instructional value; do not reproduce NAPLAN's test-heavy response balance. For each multiple-choice item, record why every distractor is plausible but wrong. For constructed responses, distinguish the expected answer, acceptable evidence, and reasoning link where needed.

Generate from one structured source record so student passages, teacher prompts, questions, answers, evidence locations, question metadata, visuals, citations, and slide ranges remain in parity. Do not draft the teacher sheet from memory after laying out student pages. Any passage revision invalidates dependent question records until they are rechecked against the final text.

## Preserve teacher-assigned groups

Use the fixed assessed profiles in [group-profiles.md](references/group-profiles.md):

- Monday: Alpha
- Tuesday: Beta
- Wednesday: Gamma
- Thursday: Delta
- Friday: Epsilon

Teacher assessment is authoritative. Do not reassess students, change membership, rename groups, infer new placements, or weaken Epsilon to Year 4/5 reading complexity. Student-facing slides and printables show only the Greek group name. Never show the assessed profile, reading level, difficulty band, day-to-level mapping, or an explanatory group description on student-facing material; those details are teacher-facing only.

## Create the actual PowerPoint outputs

Produce:

1. one Shared Reading PowerPoint for projection; and
2. one editable Guided Reading print PowerPoint containing all five teacher sheets and seven complete student copies per group.

For PowerPoint authoring, use the installed Presentations skill and its required artifact-tool, source-note, rendering, overflow, and inspection workflow. The printable deck uses exact A4 landscape geometry. Keep reading text as editable PowerPoint text and keep visuals as separate replaceable objects; never flatten an instructional page into a full-slide image.

The seven copies are embedded in the deck. Printing one copy of the complete presentation must yield one teacher sheet and seven complete student reading sets for each scheduled group. Do not tell the teacher to select seven copies in the print dialog.

## Verify and release

Maintain the layout manifest described in [the PowerPoint pack contract](references/powerpoint-pack-contract.md), then run:

```text
python scripts/audit_reading_pack.py --manifest <manifest.json> --guided-deck <guided.pptx> --shared-deck <shared.pptx> --out <audit.json>
```

Also render and inspect every slide at full size. Fix all errors before release. Structural success does not override weak differentiation, unsupported claims, cultural or Health-safety concerns, mismatched answers, weak or ambiguous distractors, unsupported inferences, unreadable pages, or unhelpful visuals.

Release only the requested final PowerPoints and a concise teacher-facing summary. Retain source and audit records in the working folder unless the user asks for them.

## Boundaries

- A missed group remains `not taught` until the teacher reschedules it.
- Relief packs omit Guided Reading unless the teacher explicitly requests otherwise.
- Morning Work, Literacy Warm-up, Shared Reading, Guided Reading, and independent reading use genuinely different passages.
- The weekly Monday workflow is a production contract, not permission to create or modify a scheduler. Configure automation only when explicitly requested.
- The supplied Technologies curriculum covers Design and Technologies. Do not silently claim Digital Technologies alignment.
- NAPLAN materials inform question construction only. Do not copy their passages or questions, reproduce their response-format balance, or turn weekly Guided Reading into standardised-test rehearsal.
