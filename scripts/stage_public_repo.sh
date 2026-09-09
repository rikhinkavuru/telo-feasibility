#!/usr/bin/env bash
# Stage the public copy of the feasibility package.
#
# The assignment requires the code to be public. The private working tree is not safe to
# publish as-is: it sits inside a repository whose history carries contact lists, and it
# carries 200 MB of raw ablation dumps that nobody needs. This script copies only the
# publishable package into a fresh tree with no history, then refuses to finish if it finds
# an email address that is not the author's own.
#
# It does NOT create a GitHub repository and it does NOT push. Publishing is a human step.
#
# Usage: bash scripts/stage_public_repo.sh [dest]   (default ~/telo-public)

set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$HOME/telo-public}"
OWN_EMAIL="rikhin@virahacks.com"

echo "staging $SRC -> $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"

rsync -a \
  --exclude '.venv/' --exclude '.git/' --exclude '__pycache__/' \
  --exclude '.mypy_cache/' --exclude '.ruff_cache/' --exclude '.pytest_cache/' \
  --exclude '.DS_Store' --exclude '*.pyc' \
  --exclude 'results/ablation/' --exclude 'results/simulation/' --exclude 'results/optimization/' \
  --exclude 'reports/simulator/template.html' \
  --exclude 'LAUNCH.md' \
  "$SRC"/ "$DEST"/

# ---- privacy gate -----------------------------------------------------------
# The scan deliberately skips data/raw_snapshots/. Those files are verbatim frozen copies of
# public federal records (the FDA shortage database, Federal Register and CFR XML) whose
# sha256 digests the reproducibility tests verify. They contain organizational contacts that
# the government itself publishes: manufacturer customer-service lines in the shortage CSV,
# and the named agency contact printed in the proposed rule. Editing them to strip an address
# would corrupt the snapshot, break every hash the package depends on, and misrepresent the
# source. Republishing a federal document unaltered is the correct handling. Everything
# outside that directory is still scanned strictly, which is where a real leak would appear.
echo "scanning for addresses (frozen public snapshots excluded, see comment above)"
HITS="$(grep -rIhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
          --exclude-dir=raw_snapshots "$DEST" 2>/dev/null \
        | sort -u | grep -v "^${OWN_EMAIL}$" | grep -v '^git@github\.com$' || true)"
ALLOW="biomap-consortium@ati.org"   # organizational contact published in a cited public source
UNEXPECTED="$(printf '%s\n' "$HITS" | sed '/^$/d' | grep -vxF "$ALLOW" || true)"
if [ -n "$UNEXPECTED" ]; then
  echo "REFUSING TO STAGE. Unexpected addresses found:" >&2
  printf '%s\n' "$UNEXPECTED" >&2
  echo "Remove them or add them to ALLOW with a written reason, then re-run." >&2
  exit 1
fi
echo "  addresses: author only, plus the allowed organizational contact"

# No contact roster may cross over. The test is content, not filename: the outreach method
# documents belong in a public methods package and carry no addresses, while a roster is
# defined by holding addresses for people who are not the author. A filename check alone
# would block the methodology and would miss a roster that was named something else.
ROSTERS=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  FOREIGN="$(grep -IhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$f" 2>/dev/null \
             | sort -u | grep -v "^${OWN_EMAIL}$" | grep -v '^git@github\.com$' \
             | grep -vxF "biomap-consortium@ati.org" || true)"
  [ -n "$FOREIGN" ] && ROSTERS="$ROSTERS$f\n"
done <<EOF
$(find "$DEST" -type f \( -iname '*outreach*' -o -iname '*contact*' -o -iname '*target*' \) \
    -not -path '*/raw_snapshots/*')
EOF
if [ -n "$ROSTERS" ]; then
  echo "REFUSING TO STAGE. A contact roster reached the public tree:" >&2
  printf '%b' "$ROSTERS" >&2
  exit 1
fi
echo "  outreach method documents present, no contact roster"

# ---- fresh history ----------------------------------------------------------
cat > "$DEST/.gitignore" <<'GITIGNORE'
.venv/
__pycache__/
*.pyc
.mypy_cache/
.ruff_cache/
.pytest_cache/
.DS_Store
results/ablation/
results/simulation/
results/optimization/
GITIGNORE

git -C "$DEST" init -q -b main
git -C "$DEST" add -A
SIZE="$(du -sh "$DEST" | cut -f1)"
FILES="$(git -C "$DEST" diff --cached --name-only | wc -l | tr -d ' ')"
echo
echo "staged: $FILES files, $SIZE, no history"
echo "review with:  git -C $DEST status"
echo "then, to publish (a human step, not an automated one):"
echo "  git -C $DEST commit -m 'Feasibility study package, initial public release'"
echo "  gh repo create <name> --public --source $DEST --push"
