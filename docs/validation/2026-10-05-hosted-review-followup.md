# Hosted review follow-up


The 28-test run above is the preserved publication checkpoint at `83fe5c81e382468f34f9b447fa4af56ac0bffc0d`. A subsequent hosted review identified a real cross-field gap in the published level schema. The schema now rejects all 20 mismatched role/group combinations and accepts the five assigned pairs, matching the Python validator. Four focused regression/contract tests bring the current suite to **32 tests, all passing**. JSON Schema checks use the declared development-only dependency in `requirements-dev.txt`; the production validator remains standard-library-only.

Teacher override wording is also clarified: an explicit request is recorded for the teacher, but the current validator has no override input and the request cannot waive current level/parity PASS requirements. No bypass was added. The writer's authority sentence now uses an explicit grammatical subject without changing its prohibition on self-approval.

The hosted review's claim that behavioural runs were still pending referred to an earlier PR description. The current description records the independent outcomes and links to the committed evidence. The original corpus remains unresolved, as reported above. GitHub Actions run [37345006215](https://github.com/Malajusa/dlp-guided-reading/actions/runs/37345006215) is a completed Copilot code review; it is not an execution of the deterministic test suite.

### Reproducing the checks

Install the test-only dependency in a development environment, then run the complete suite:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

The committed evidence is an external recorded behavioural run, not a claim that unittest dispatches language-model reviewers. It includes every blinded input, actual output, frozen expectation, diagnostic finding, schema/hash check and forward revision. Model judgements may vary on a fresh run; mechanically replaying records does not create new independent-agent evidence.

The exact forward package and stale-state negative check can be replayed from the committed evidence:

```sh
python - <<'PYCODE'
import copy, json
from pathlib import Path
from scripts.validate_pitch_review_package import validate_review_package
record = json.loads(Path('docs/validation/2026-10-05-level-pitch-evidence.json').read_text())
package = record['forward_test']['pitch_review_package']
assert validate_review_package(package)['status'] == 'PASS'
stale = copy.deepcopy(package)
stale['passages']['Epsilon']['text'] += '\nA wording change after approval.'
assert validate_review_package(stale)['status'] == 'FAIL'
for case in record['behavioural_cases']:
    result = case['result']
    print(result['case_id'], result['actual_verdict'], result['verdict_matches'], result['evidence_qualification'])
PYCODE
```

This replay deliberately exposes the five positive mismatches and two invalid-prerequisite cases; it does not turn them into behavioural passes. The original evidence file remains frozen. New corpus work is separately versioned.


