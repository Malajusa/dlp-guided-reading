# Weekly PowerPoint Pack Contract

## Deliverables

Create two editable PowerPoint files for the following teaching week:

1. `Shared_Reading_T<term>_W<week>.pptx` for whole-class projection.
2. `Guided_Reading_Print_T<term>_W<week>.pptx` as the single print document.

PowerPoint is authoritative. A PDF may be produced as a temporary render or print check, but it is not the primary deliverable unless requested.

## Guided Reading print deck geometry

- exact A4 landscape: 29.7 cm wide by 21.0 cm high;
- one slide equals one printed sheet;
- all text remains editable PowerPoint text;
- visuals remain separate, replaceable objects;
- no full-slide flattened page images;
- one consistent, highly legible body typeface and stable hierarchy;
- no unintended bleed, clipping, overlap, or printer-edge content.

Use the Presentations skill's current local PowerPoint workflow. Render every slide and inspect it individually at full size. Run its overflow checks in addition to the skill audit.

## Required print order

For each group in timetable order:

1. exactly one teacher sheet;
2. student copy 1 as a complete ordered reading;
3. student copy 2 as a complete ordered reading;
4. continue through student copy 7.

Then begin the next group. Do not insert cover, divider, instruction, or blank slides unless the user requests them. If the reading has multiple pages, repeat the entire page sequence seven times. Printing one copy of the whole deck must produce the correct physical quantity.

Order:

- Monday Alpha;
- Tuesday Beta;
- Wednesday Gamma;
- Thursday Delta;
- Friday Epsilon.

Use a restrained footer on student pages to aid collation: `<Group> | copy <n> of 7 | page <p> of <total>`.

Student-facing slides and printables identify the group only by its Greek name. Do not display `very low`, `low`, `at level`, `above level`, `Year 9 reading level`, equivalent difficulty language, assessed profiles, explanatory group descriptions, or a key that maps Greek names to levels. These details may appear on teacher sheets and internal records only.

## Shared Reading deck

Use the Daily Lesson Pack projected-reading geometry and visual system active at generation time. Shared Reading does not need A4 print geometry unless the user explicitly requests it.

After any optional title or orientation slide recorded in the manifest, alternate strictly:

1. paragraph plus exactly one question;
2. matched answer;
3. next paragraph plus exactly one question;
4. matched answer.

Keep paragraphs readable when projected. The complete answer is visually dominant. An answer slide may include one short evidence explanation but cannot add a new paragraph or question.

Design each question using [the NAPLAN-informed question design standard](naplan-reading-question-design.md). The standard informs question quality and evidence reasoning only; it does not require NAPLAN-style formatting or multiple-choice dominance.

## Working source record

Before layout, maintain a structured record containing:

- target dates, term, week, and timetable;
- prescribed Reading Focus, Learning Intention, and Success Criteria from `references/40-week-reading-overview.md`;
- any explicit teacher-authorised departure from the overview, with the teacher instruction recorded verbatim or faithfully summarised;
- curriculum source area, topic, codes where used, and selection rationale;
- genre and specific Writing features;
- previously taught comprehension processes deliberately spiralled into the week's reading;
- intended evidence distance and response depth;
- verified facts, source URLs/titles, dates, qualifications, and visual provenance;
- Shared Reading paragraphs and one structured question record per question/answer pair;
- for each group: final passage pages, vocabulary/morphology, model, stops, structured question records, prompts, misconceptions, assessment focus, next step, and visual plan;
- final slide ranges and copy ranges.

Each substantive question record contains at minimum:

```json
{
  "id": "GAMMA-Q2",
  "question_type": "inference",
  "target_reasoning": "Combine the character's action with the later reaction to infer motive",
  "evidence_location": "paragraphs 2 and 4",
  "evidence_distance": "distributed",
  "response_mode": "constructed",
  "expected_answer": "...",
  "acceptable_evidence": ["..."],
  "reasoning_link": "..."
}
```

Use the taxonomy and evidence-distance values in `references/naplan-reading-question-design.md`. `reasoning_link` may be brief or omitted only when the relationship between evidence and answer is self-evident.

For a multiple-choice question, also record:

```json
{
  "correct_option": "B",
  "distractors": [
    {"option": "A", "error_model": "surface match", "why_wrong": "..."},
    {"option": "C", "error_model": "partial evidence", "why_wrong": "..."},
    {"option": "D", "error_model": "unsupported inference", "why_wrong": "..."}
  ]
}
```

Every distractor must be plausible but demonstrably wrong for a text-based reason. Do not use joke answers, giveaway wording, or ambiguous alternatives.

Generate teacher and student content from this record. Any passage revision invalidates dependent questions, answers, evidence locations, evidence distances, distractor rationales, vocabulary references, and layout ranges until rechecked. Assessment evidence may refine how the prescribed weekly focus is taught; it does not silently replace the focus.

## Layout manifest

Create a JSON manifest for deterministic auditing. Example shape:

```json
{
  "schema_version": "1.0",
  "term": 1,
  "week": 2,
  "reading_focus": "Main idea and supporting details",
  "learning_intention": "Identify what a paragraph is mainly about and distinguish supporting information.",
  "success_criteria": "I can state the main idea and select details that genuinely support it.",
  "writing_genre": "narrative",
  "content_area": "Health",
  "shared_reading": {
    "lead_slides": [1],
    "pairs": [
      {"question_slide": 2, "answer_slide": 3}
    ]
  },
  "guided_reading": {
    "groups": [
      {
        "group": "Alpha",
        "day": "Monday",
        "profile": "very low",
        "visual_support": "strongest",
        "teacher_slide": 1,
        "student_copies": [[2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15]],
        "epsilon_visual_exceptions": []
      }
    ]
  }
}
```

Add all five groups. Slide ranges are inclusive and one-based. `epsilon_visual_exceptions` is empty for Alpha-Delta. For Epsilon, each permitted entry has this form:

```json
{
  "page": 1,
  "kind": "scientific_or_technical_diagram",
  "purpose": "Shows the labelled parts students must compare",
  "source": "Authoritative source title or URL"
}
```

`page` is the page position within each Epsilon student copy, not the absolute slide number.

The layout manifest remains deliberately structural. Keep the richer semantic question records in the working source record rather than pretending the deterministic layout audit can judge question quality.

## Deterministic audit

Run `scripts/audit_reading_pack.py` with the final decks and manifest. It checks:

- A4 landscape guided-deck geometry;
- exact group/day/profile/order;
- exactly one teacher slide and seven complete copies per group;
- contiguous slide coverage with no unrecorded pages;
- matching page counts and content signatures across the seven copies;
- editable text presence on student pages;
- likely adjacent-group duplication;
- undeclared Epsilon embedded images;
- Shared Reading question/answer pair order;
- likely passage reuse between Shared and Guided Reading.

Treat warnings as required review, not automatic permission to release. The audit cannot judge instructional quality, factual truth, cultural authority, question validity, distractor quality, crop quality, visual usefulness, or whether the recorded Reading Focus, Learning Intention, and Success Criteria match the overview.

## Final manual gates

- Confirm the recorded Reading Focus, Learning Intention, and Success Criteria match the target term/week in `references/40-week-reading-overview.md`, unless an explicit teacher override is recorded.
- Inspect every final question against its structured question record and the final student text or visual.
- Confirm each answer is defensible, the evidence location/distance is accurate, and any required reasoning link is valid.
- For every multiple-choice item, confirm all distractors are plausible, distinct, and demonstrably wrong for text-based reasons.
- Confirm question wording does not introduce accidental difficulty unrelated to the intended reading process.
- Inspect all slides at full size, including every embedded duplicate.
- Confirm every teacher prompt and answer against the displayed final student wording.
- Confirm visuals match the final text and do not reveal intended inferences.
- Confirm Alpha-Epsilon represent genuine progression without loss of the shared idea.
- Confirm PowerPoint objects remain editable and the deck opens without repair warnings.
- Print-preview at one copy and verify the physical sequence and quantities.
