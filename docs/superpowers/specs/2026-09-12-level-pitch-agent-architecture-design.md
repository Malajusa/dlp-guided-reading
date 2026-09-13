# Level-Specific Pitch Agent Architecture

Date: 2026-09-12
Status: Approved in principle; implementation not yet started

## Purpose

Add independent level-specific review agents to the Guided Reading workflow so each Alpha-Epsilon passage is explicitly checked for correct pitch, accessibility, age-appropriateness, and fidelity to the common conceptual destination before layout.

The design deliberately separates drafting from approval. A passage writer must not approve its own text.

## Architectural summary

The weekly workflow becomes:

1. Weekly Blueprint Resolver establishes the authoritative Reading Focus, Learning Intention, Success Criteria, curriculum context, conceptual spine, factual source record, visual constraints, and provisional question-intent targets such as intended reasoning, evidence distance, and response depth.
2. Central Passage Writer drafts five distinct Alpha-Epsilon rewrites from the same blueprint.
3. Five Level Pitch Review Agents inspect their assigned passage independently:
   - Alpha Pitch Agent
   - Beta Pitch Agent
   - Gamma Pitch Agent
   - Delta Pitch Agent
   - Epsilon Pitch Agent
4. Any agent returning `REVISE` or `REJECT` sends a structured revision request back to the Central Passage Writer.
5. The revised passage returns to the same level agent. A passage cannot advance without `PASS` bound to the exact reviewed passage.
6. When all five passages pass individually, a Progression and Parity Agent compares them side-by-side.
7. Final question writing and the existing question-design/evidence QA operate on the approved texts.
8. PowerPoint generation, deterministic audit, render inspection, and release QA follow as already specified.

The five level reviews should run in parallel when the runtime supports independent parallel agent dispatch. A sequential fallback is acceptable only if each reviewer remains isolated from neighbouring draft texts and other reviewers' verdicts until its own verdict is complete.

## Authority model

### Central Passage Writer

Owns drafting and revision only. It must:

- preserve the weekly conceptual spine and verified factual content;
- produce five genuine rewrites rather than cosmetic edits;
- respect group-profile constraints;
- revise only the passage(s) identified by reviewers unless a shared factual or conceptual defect affects all five;
- never self-certify pitch.

### Level Pitch Review Agents

Each level agent owns approval authority for one group only. It returns exactly one verdict:

- `PASS` — text is appropriately pitched and may proceed;
- `REVISE` — repairable pitch defects exist; the agent must identify concrete changes required;
- `REJECT` — the text is fundamentally mis-pitched, loses the common concept, introduces inappropriate content, or cannot be repaired safely with local edits.

A reviewer must evaluate the final wording it is asked to approve, not a summary of the passage. Its approval is valid only for the exact passage hash recorded in its review.

### Progression and Parity Agent

Owns cross-level comparison after all five level agents pass. It may return:

- `PASS` — progression is coherent and conceptual parity is preserved;
- `REVISE_LEVELS` — one or more specified passages need revision;
- `REJECT_SET` — the five-text set has a systemic design defect requiring redrafting from the shared blueprint.

It cannot lower or raise teacher-assigned group placements. Its verdict is bound to the exact set of five passage hashes it reviewed.

## Common review dimensions

Every level agent evaluates:

- decoding and word-recognition demand;
- unfamiliar multisyllabic and multimorphemic vocabulary;
- morphology burden and whether support is appropriate;
- sentence length, clause structure, and syntactic density;
- cohesion and referent tracking;
- paragraph density and information packing;
- assumed background knowledge;
- explicitness of essential meaning;
- evidence distance;
- inference demand;
- ambiguity and competing plausible interpretations;
- text structure/navigation demands;
- likely fluency burden;
- response depth implied by the provisional question-intent targets;
- age-appropriateness and dignity of subject matter;
- appropriateness of visual support;
- preservation of the weekly Learning Intention, Success Criteria, factual integrity, and common conceptual destination.

Text length is evidence but never the primary pitch criterion.

## Group-specific authority and failure conditions

### Alpha Pitch Agent

Target: very low reading access with age-respectful Year 4/5 content.

The agent expects:

- mostly immediate/local evidence;
- short, clearly related clauses;
- explicit referents and connectives;
- controlled new vocabulary and morphology;
- essential background knowledge supplied in the passage or teacher introduction;
- strong purposeful visual support where useful;
- worthwhile thinking without avoidable decoding overload.

Reject or revise when:

- essential meaning depends on distant inference;
- syntax or cohesion obscures who/what is being referred to;
- unfamiliar vocabulary density overwhelms the instructional target;
- the passage becomes infantile or strips away the worthwhile concept;
- the passage states the intended answer so directly that the weekly comprehension focus disappears.

### Beta Pitch Agent

Target: low reading access with increasing independence.

The agent expects:

- local to paragraph-level evidence;
- selected unfamiliar multisyllabic/multimorphemic words with planned support;
- simple, compound, and short complex sentences;
- mostly explicit cohesion with some independent referent tracking;
- meaningful but scaffoldable inference.

Reject or revise when:

- the text still behaves like the documented Alpha profile with only harder vocabulary added;
- the text approaches independent year-level demand without enough Beta-appropriate access support;
- difficulty is added mainly through vocabulary substitution;
- evidence remains so immediate that the intended Beta reasoning progression is absent.

### Gamma Pitch Agent

Target: independent Year 4/5 reading demand.

The agent expects:

- varied sentence structures;
- meaningful paragraphing and genre-appropriate navigation;
- some unfamiliar technical or literary vocabulary;
- paragraph/distributed evidence where appropriate;
- literal and implied meaning;
- independent evidence location and complete explanation.

Reject or revise when:

- the text is noticeably simplified below Year 4/5 expectations;
- teaching support has been embedded into the prose to the point of removing independence;
- the passage lacks enough independent evidence location or implied meaning to represent the documented Gamma profile;
- the passage relies on specialist knowledge not supplied or reasonably inferable.

### Delta Pitch Agent

Target: above-level reading demand without changing the age-appropriate topic.

The agent expects:

- increased syntactic density and information packing;
- more precise or abstract vocabulary;
- less explicit cohesion;
- distributed evidence and evidence integration;
- qualified claims, subtle motivation, or multiple plausible interpretations where appropriate;
- synthesis, comparison, justification, or evaluation rather than merely longer responses.

Reject or revise when:

- `above level` is represented mainly by length or technical vocabulary;
- reasoning demand does not meaningfully exceed the documented Gamma profile;
- unnecessary obscurity replaces legitimate complexity;
- the text drifts into older-student subject matter rather than harder reading.

### Epsilon Pitch Agent

Target: Year 9 reading complexity applied to age-appropriate Year 4/5 subject matter.

The agent expects:

- sophisticated syntax and dense cohesion;
- nuanced, precise, and sometimes abstract vocabulary;
- implicit relationships and distal evidence;
- ambiguity or competing perspectives where the weekly focus supports them;
- whole-text or cross-text reasoning where appropriate;
- evaluation of credibility, authorial choices, or evidence quality;
- no decorative/narrative illustration; only necessary functional scientific/technical diagrams.

Reject or revise when:

- the passage is simply longer than the documented Delta profile would require;
- it reads like an ordinary Year 5 text with harder vocabulary inserted;
- relationships and conclusions are over-explained;
- evidence is predominantly immediate/local without a pedagogical reason;
- age-inappropriate curriculum or themes are introduced to simulate Year 9 difficulty;
- a visual lowers the intended prose demand.

## Review input contract

Each level agent receives only the information needed to judge its assigned passage accurately:

- target group and teacher-assigned profile;
- final candidate passage;
- weekly Reading Focus, Learning Intention, and Success Criteria;
- common conceptual spine and essential factual claims;
- genre/text form;
- provisional question-intent metadata, such as intended reasoning, evidence distance, and response depth, without requiring final question wording;
- visual plan for that group;
- relevant group-profile rules and adjacent profile definitions for boundary reference;
- any explicit teacher-supplied point-of-need notes.

The agent does not receive neighbouring candidate passages, other reviewers' verdicts, permission to change placement, or permission to redesign the weekly sequence.

## Review output schema

Each agent returns a machine-readable record with this logical shape:

```json
{
  "reviewer_role": "gamma-pitch-reviewer",
  "group": "Gamma",
  "passage_sha256": "...",
  "verdict": "PASS | REVISE | REJECT",
  "pitch_summary": "short evidence-based judgement",
  "dimension_findings": {
    "decoding": "pass or issue",
    "vocabulary_morphology": "pass or issue",
    "syntax": "pass or issue",
    "cohesion": "pass or issue",
    "background_knowledge": "pass or issue",
    "evidence_distance": "pass or issue",
    "inference_ambiguity": "pass or issue",
    "response_demand": "pass or issue",
    "age_appropriateness": "pass or issue",
    "visual_support": "pass or issue",
    "conceptual_parity": "pass or issue"
  },
  "blocking_issues": [],
  "required_revisions": [],
  "non_blocking_notes": []
}
```

`PASS` is invalid if `blocking_issues` or `required_revisions` is non-empty. A `PASS` whose `passage_sha256` does not match the passage entering the next stage is invalid.

Revision instructions must be specific enough for the writer to act on without guessing, but must not rewrite the whole passage unless `REJECT` is necessary.

## Revision loop

The same reviewer that identified a defect must re-review the revision.

Maximum normal loop: three revision cycles per passage. After three unsuccessful cycles, the orchestrator escalates to `REJECT` and requires a fresh redraft from the blueprint rather than accumulating patchwork edits.

Any wording change produces a new passage hash and invalidates the prior level approval. Any revision that changes evidence locations, answerability, or wording relied on by questions also invalidates dependent question records and sends them back through question/evidence QA.

## Progression and Parity Agent

After five individual passes, compare all five texts for:

- monotonic but not mechanical progression in access and reasoning demand;
- appropriate decrease in visual support;
- no adjacent-group duplication or cosmetic rewriting;
- no abrupt unjustified difficulty jumps;
- preservation of the same essential knowledge and conceptual destination;
- no loss of worthwhile content in Alpha/Beta;
- no topic drift in Delta/Epsilon;
- question/evidence demand progressing alongside passage complexity;
- Epsilon representing genuinely advanced reading complexity rather than merely more words.

The cross-level reviewer may not override a level agent by declaring a failed passage acceptable. It may only add further revision requirements.

Its output records all five passage hashes. Any subsequent change to any passage invalidates the parity approval and requires a new cross-level review after the affected level re-passes.

## Information barriers

To preserve reviewer independence:

- level agents do not see the writer's self-assessment;
- each level agent reviews only its own candidate passage, while profile definitions may be used as boundary references;
- level agents do not see neighbouring candidate passages;
- level agents do not see other reviewers' verdicts before issuing their own;
- only the Progression and Parity Agent receives all five individually approved passages together;
- teacher-assigned profiles are authoritative and cannot be inferred or renegotiated by agents.

## Failure handling

Release is blocked when:

- any level lacks a valid `PASS` from its assigned agent;
- a level approval hash does not match the passage being advanced;
- the Progression and Parity Agent does not return `PASS` for the current five passage hashes;
- a passage changed after approval without re-review;
- the passage/question pair changed without question/evidence re-validation;
- reviewer output is malformed or omits required dimensions;
- a reviewer attempts to change group placement or the 40-week sequence.

On agent disagreement, do not average verdicts. The stricter blocking judgement stands until the relevant passage is revised or the teacher explicitly overrides it.

Teacher override must be recorded in the source record, including which gate was overridden and why.

## Proposed repository structure

Implementation should keep orchestration separate from role definitions:

```text
agents/
  openai.yaml
  roles/
    central-passage-writer.md
    alpha-pitch-reviewer.md
    beta-pitch-reviewer.md
    gamma-pitch-reviewer.md
    delta-pitch-reviewer.md
    epsilon-pitch-reviewer.md
    progression-parity-reviewer.md
  schemas/
    pitch-review.schema.json
    progression-review.schema.json
    orchestration-state.schema.json
references/
  agent-orchestration.md
```

`SKILL.md` should describe when the orchestration runs and the release gates, while detailed role instructions remain in focused files.

## Testing strategy

Implementation must be tested with adversarial and boundary examples, not only ideal passages.

Minimum test matrix:

1. Alpha passage that is childish but easy — Alpha agent must reject/revise.
2. Alpha passage with dense syntax but short word count — must reject/revise.
3. Beta passage that merely imitates the Alpha profile with harder words — Beta agent must reject/revise.
4. Gamma passage simplified below Year 4/5 demand — Gamma agent must reject/revise.
5. Delta passage that only increases length or vocabulary beyond Gamma — Delta agent must reject/revise.
6. Epsilon passage that is a long Year 5 text — Epsilon agent must reject/revise.
7. Epsilon passage with Year 9 topic but ordinary syntax — must reject/revise for topic drift and false pitch.
8. Correctly pitched examples for all five — each assigned agent must pass its own level.
9. Five individually acceptable texts with Beta/Gamma near-duplication — parity agent must block.
10. Five texts with conceptual content removed from Alpha — parity agent must block.
11. Revision changes evidence relied upon by questions — question records must be invalidated and rechecked.
12. Reviewer attempts to change teacher placement — orchestration must reject that action.
13. Passage changes after `PASS` — stale hash must invalidate the approval.
14. Parity-approved set changes one passage — parity approval must be invalidated.

Forward validation should then regenerate the recent Term 3 Week 9 pack and test whether the Epsilon under-pitch and Alpha over-explicitness identified in manual review are caught before layout.

## Non-goals

This subsystem does not:

- change the Alpha-Epsilon placements;
- assess students or infer new groups;
- replace the 40-week overview;
- replace factual/cultural/source QA;
- replace NAPLAN-informed question-design QA;
- replace PowerPoint structural and visual auditing;
- create separate subject matter for higher groups;
- expose group levels on student-facing materials.

## Success criteria

The subsystem is ready for release when:

- all five reviewers reliably distinguish correctly pitched texts from the specified mis-pitch cases;
- writer/reviewer independence is enforced;
- approvals are cryptographically bound to the exact reviewed passage text;
- revision loops fail closed;
- progression/parity defects are caught after individual passes;
- parity approval is bound to the exact five-text set;
- no passage can reach final question/layout generation without required approvals;
- the existing weekly pack contracts remain intact;
- the Term 3 Week 9 forward test demonstrates that previously observed pitch defects are caught upstream rather than during final manual inspection.
