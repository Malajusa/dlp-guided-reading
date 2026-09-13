# Weekly PowerPoint Pack Contract

## Deliverables

Create two editable PowerPoints: `Shared_Reading_T<term>_W<week>.pptx` and `Guided_Reading_Print_T<term>_W<week>.pptx`.

## Guided Reading print geometry and order

Use exact A4 landscape, one slide per sheet, editable text and separate replaceable visuals. For each group in Monday Alpha, Tuesday Beta, Wednesday Gamma, Thursday Delta, Friday Epsilon order: one teacher sheet followed by seven complete student copies. No unrequested divider/blank slides.

Student pages show only Greek group names, never profile/difficulty labels.

## Shared Reading

Use the active Daily Lesson Pack projected-reading geometry. After optional lead slides, alternate paragraph+one question then matched answer. Answers must be grounded in the displayed paragraph. Apply the NAPLAN-informed question design standard.

## Working source record

Before layout retain:

- target dates, term, week and timetable;
- prescribed Reading Focus, Learning Intention and Success Criteria;
- curriculum source/topic/genre and verified sources;
- common conceptual spine and provisional question-intent targets;
- any explicit **teacher override** and reason;
- for each group: final passage pages, visual plan, `passage_sha256`, `revision_cycle`, current `pitch_review`, question records, prompts, misconceptions, assessment focus and next step;
- one set-level `progression_review` containing all five current hashes;
- final slide/copy ranges.

Example group record:

```json
{
  "passage_sha256": "...",
  "revision_cycle": 1,
  "pitch_review": {
    "reviewer_role": "alpha-pitch-reviewer",
    "verdict": "PASS",
    "passage_sha256": "..."
  }
}
```

A wording change invalidates the prior level review and set-level progression review. If it changes evidence or answerability, dependent **question records** are invalid and must be rechecked. Maximum normal loop is **three revision cycles** before fresh redraft.

Before PowerPoint layout, build the pitch-review package and run:

```text
python scripts/validate_pitch_review_package.py --package <pitch-review-package.json> --out <pitch-review-audit.json>
```

Require `pitch-review-audit.json` status `PASS`. Keep this separate from the structural layout manifest and `audit_reading_pack.py`.

## Layout manifest

Maintain schema version 1.0 with term/week, Reading Focus/Learning Intention/Success Criteria, Shared Reading lead/pair slides, and Guided Reading group/day/profile/visual-support/teacher-slide/student-copy ranges. Epsilon visual exceptions are restricted to necessary scientific/technical diagrams with purpose and source.

## Deterministic audit

After layout run `scripts/audit_reading_pack.py`. It checks A4 geometry, group order, teacher/copy counts, slide coverage, duplicate-copy parity, editable text, likely passage duplication, Epsilon image restrictions, Shared Reading pair order, and likely Shared/Guided passage reuse.

## Final manual gates

- pitch-review audit is PASS and corresponds to final text;
- five current level passes and current progression/parity pass are retained;
- questions match final text/evidence;
- visuals do not reveal intended inferences;
- Alpha-Epsilon show genuine progression with conceptual parity;
- every slide is inspected at full size;
- PowerPoint opens without repair warnings;
- one-copy print preview yields the required physical quantity.
