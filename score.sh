#!/usr/bin/env bash
# Score an agent's lifecycle.py against the hidden acceptance tests.
# Usage: ./score.sh /path/to/agent/repo   (folder that contains lifecycle.py)
set -u
REPO="$(cd "${1:?usage: ./score.sh /path/to/folder/with/lifecycle.py}" && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$REPO/lifecycle.py" ] || { echo "no lifecycle.py in $REPO"; exit 2; }
cd "$HERE/task/tests" || exit 2
for grp in stated edge; do
  out=$(PYTHONPATH="$REPO" python3 -m pytest -q -m "$grp" -p no:cacheprovider 2>&1 | tail -1)
  echo "$grp: $out"
done
echo "--- failing tests (all) ---"
PYTHONPATH="$REPO" python3 -m pytest -q -p no:cacheprovider 2>&1 | grep -E "^FAILED" || echo "none"
echo "--- size ---"
wc -l "$REPO/lifecycle.py"
[ -f "$REPO/test_lifecycle.py" ] && wc -l "$REPO/test_lifecycle.py"
true
