# Daily Lesson Pack Integration Contract

Read this only when packaging, installing, or updating the Daily Lesson Pack umbrella. It is not part of ordinary weekly content generation.

## Development boundary

This repository is the development source for the coordinated weekly Shared and Guided Reading generator. Do not edit the installed Daily Lesson Pack merely because this repository changes. Installation or umbrella integration requires an explicit request, package validation, staged replacement, and rollback path.

## Required umbrella changes at integration

1. Replace the installed timetable-only `dlp-guided-reading` contract with this production skill after release QA.
2. Reconcile `dlp-shared-reading` ownership so a weekly reading-pack request has one authoritative generator. Preserve its paragraph/question/answer evidence rules; do not allow two skills to generate competing Shared Reading decks.
3. Update the Daily Lesson Pack orchestrator so it can consume the already-generated weekly Shared Reading deck and record the scheduled Guided Reading group without regenerating or duplicating the weekly resources.
4. Add the Shared Reading deck, Guided Reading print deck, layout manifest, deterministic audit, and full rendered inspection to component acceptance and final pack QA.
5. Preserve Morning Work, Literacy Warm-up, Shared Reading, Guided Reading, and independent-reading passage independence.
6. Preserve the Monday Alpha through Friday Epsilon timetable labels in daily packs while keeping assessed descriptions teacher-facing.
7. Keep relief-pack omission and `not taught` status behaviour unless the teacher explicitly changes them.

## Monday production workflow

The intended recurring job runs Monday morning and creates the following teaching week's two PowerPoints. The scheduler prompt must require authoritative term/week resolution, current planning inputs, assessment exceptions, both final decks, and a passing audit. A scheduled job must not guess a week when school-calendar or plan data is unresolved.

Do not create or modify an automation while installing the skill unless the user separately requests scheduling.

## Release gate

Before integration:

- validate this skill independently;
- forward-test at least one Weeks 1-6 curriculum-aligned pack and one post-Week-6 assessment-responsive pack;
- verify pack copy counts, editable text, visual progression, teacher/student parity, and source records;
- audit dependency closure and package paths;
- stage the installation outside the live skill directory;
- retain a recoverable rollback copy outside the live skills tree;
- compare staged, installed, and repository hashes.

An integrated release is not production-authoritative until the Daily Lesson Pack release-status record says so.
