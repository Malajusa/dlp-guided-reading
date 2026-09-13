# Shared and Guided Reading Production Standard

Status: governing development standard, version 2.2. This skill remains a development component until release review and deliberate Daily Lesson Pack integration.

## 1. Instructional priority

This is a reading program informed by curriculum content, not a content-area worksheet delivered through a passage. Reading needs and the prescribed weekly focus control text design; curriculum content supplies worthwhile knowledge and context.

## 2. Shared and Guided Reading relationship

Shared Reading provides whole-class teacher-mediated access and models the weekly comprehension move. Guided Reading uses five distinct rewrites of one conceptual spine with group-specific vocabulary, morphology, fluency, comprehension and response demands. Shared and Guided passages must remain distinct.

## 3. Genuine rewrites

Before writing, define essential knowledge, source-supported facts, genre, vocabulary, intended comprehension opportunity, visual information, provisional question-intent targets and evidence students must locate/connect/infer/synthesise/evaluate.

Every group receives a genuine rewrite. Control decoding, morphology, vocabulary, syntax, cohesion, paragraph density, background knowledge, inference distance, ambiguity, structure, navigation, fluency and response depth. Word count alone is not differentiation.

## 4. Pitch-review gate

Before final question writing or layout, run the workflow in `agent-orchestration.md`.

Required release evidence:

- **five current level** `PASS` records, one per Alpha-Epsilon passage;
- each `PASS` bound to the exact final **passage hash**;
- a current **progression/parity** `PASS` bound to all five exact hashes;
- no **stale** approval after a wording change;
- no more than **three revision cycles** before a fresh redraft;
- any explicit **teacher override** recorded with the overridden gate and reason;
- dependent **question records** invalidated and rechecked after passage changes that affect evidence or answerability;
- a `PASS` audit from `scripts/validate_pitch_review_package.py`.

Semantic pitch approval is owned by the specialist review agents. Hash/current-state validity is checked mechanically by `validate_pitch_review_package.py`. The writer never self-approves.

## 5. Core Guided Reading sequence

Each teacher sheet supports brief knowledge activation, high-value vocabulary/morphology, a teacher model, supported first reading, targeted rereading, evidence-based discussion, concise Writing transfer during Weeks 1-6, and one manageable assessment note/next step.

## 6. Question design

Use `naplan-reading-question-design.md`. Record question type, target reasoning, evidence location/distance, expected answer, acceptable evidence, response mode and reasoning link where needed. Multiple-choice distractors must be plausible but textually wrong; constructed responses distinguish answer, evidence and reasoning.

## 7. Teacher and student material

Provide exactly one A4 landscape teacher sheet for each group and complete age-respectful student reading pages. Student materials show only Greek group names. Teacher questions/answers/evidence must match the final approved student text exactly.

## 8. Factual, cultural and Health integrity

Verify non-trivial claims and illustrations with credible authoritative sources. Do not invent cultural authority or restricted knowledge. Sensitive Health topics are opt-in only.

## 9. Accessibility and visuals

Keep instructional text editable/searchable, use strong contrast and consistent hierarchy, and use visuals only when they add comprehension value. Apply group-profile visual-support rules. Epsilon has no decorative/narrative illustration; only necessary functional scientific/technical diagrams.

## 10. Status and timetable

Default rotation is Monday Alpha, Tuesday Beta, Wednesday Gamma, Thursday Delta, Friday Epsilon. A missed session is `not taught`; relief packs omit Guided Reading unless explicitly requested.

## 11. Blocking failures

Do not release when any of these remain:

- missing, malformed, non-PASS, or stale level pitch approval;
- any level PASS whose passage hash differs from final text;
- missing, non-PASS, or stale progression/parity approval;
- a fourth unsuccessful patch cycle without fresh redraft;
- reviewer attempt to change teacher-assigned placement;
- pitch-review mechanical audit not PASS;
- identical/cosmetically altered group passages;
- Shared Reading passage reused in Guided Reading;
- teacher/student question, answer, evidence, vocabulary or pagination mismatch;
- substantive question without defensible answer/evidence;
- unsupported factual/cultural claims;
- Epsilon decorative imagery;
- flattened instructional text;
- unreadable typography, clipping, overlap or inconsistent geometry;
- incorrect physical copy counts;
- incomplete teacher sheet;
- deck not passed by deterministic checks and full rendered inspection.
