---
name: dlp-guided-reading
description: Generate and quality-assure next-week Shared Reading and differentiated Alpha-Epsilon Guided Reading PowerPoint packs for a WA Year 4/5 class within the Daily Lesson Pack. Use for weekly reading-pack planning or production; do not assess students, change teacher placements, or generate a generic daily reading passage.
---

# Weekly Shared and Guided Reading Pack

Create the following teaching week's coordinated reading pack. Reading instruction is the priority; HASS, Health, and Design and Technologies supply worthwhile knowledge and contexts.

Read the references required by the task:

- Always read [the production standard](references/production-standard.md).
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
4. detailed weekly plans;
5. the whole-year plan and [curriculum map](references/curriculum-map.md);
6. standing defaults in this skill.

If no detailed weekly plan exists for Weeks 1-6, select and sequence a suitable subtopic from the term curriculum. Record the selection and rationale in the teacher-facing source record. After Week 6, assessment evidence determines the reading focus; use curriculum-area balance only as a tie-breaker when multiple texts serve the same need.

## Build one coordinated weekly sequence

Establish one weekly blueprint before drafting:

- curriculum source area and precise topic;
- essential facts, concepts, vocabulary, and source evidence;
- current Writing genre and useful features during Weeks 1-6;
- whole-class comprehension model for Shared Reading;
- common conceptual spine for Guided Reading;
- group-specific reading targets and access controls;
- visual purposes and cultural or safety constraints.

Shared and Guided Reading must use distinct passages. They may share the topic, genre, knowledge, and selected vocabulary. Shared Reading explicitly models a useful meaning-making move; Guided Reading provides five genuine rewrites through which students apply or extend the learning at the teacher-assigned level.

Generate from one structured source record so student passages, teacher prompts, answers, evidence locations, visuals, citations, and slide ranges remain in parity. Do not draft the teacher sheet from memory after laying out student pages.

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

Also render and inspect every slide at full size. Fix all errors before release. Structural success does not override weak differentiation, unsupported claims, cultural or Health-safety concerns, mismatched answers, unreadable pages, or unhelpful visuals.

Release only the requested final PowerPoints and a concise teacher-facing summary. Retain source and audit records in the working folder unless the user asks for them.

## Boundaries

- A missed group remains `not taught` until the teacher reschedules it.
- Relief packs omit Guided Reading unless the teacher explicitly requests otherwise.
- Morning Work, Literacy Warm-up, Shared Reading, Guided Reading, and independent reading use genuinely different passages.
- The weekly Monday workflow is a production contract, not permission to create or modify a scheduler. Configure automation only when explicitly requested.
- The supplied Technologies curriculum covers Design and Technologies. Do not silently claim Digital Technologies alignment.
