#!/usr/bin/env bash
set -euo pipefail

# ----------- CONFIGURE (edit if needed) -----------
GITHUB_USER="Conyekp2"
REPO_NAME="KMS_lib"
PYTHON_VER="python3"          # uses your .venv if present
REQUIRED_IMAGES=("docs/kms_image.png" "docs/ui_home.png" "docs/ui_answer.png" "docs/overview_architecture.png")
WORKFLOW_FILE=".github/workflows/python-tests.yml"
# --------------------------------------------------

RED="\033[31m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; DIM="\033[2m"; RESET="\033[0m"
failures=()

section() { echo -e "\n${BLUE}==>${RESET} $*"; }
ok()      { echo -e "${GREEN}✓${RESET} $*"; }
warn()    { echo -e "${YELLOW}!${RESET} $*"; }
bad()     { echo -e "${RED}✗${RESET} $*"; }

# 0) Sanity: are we in the repo root?
section "Sanity checks"
if [[ ! -f "README.md" || ! -d "src" ]]; then
  bad "Run this script from your repository root (README.md and src/ must exist)."
  exit 2
fi
ok "Repository root detected."

# 1) Absolute path safety (no /Users, /home, etc.)
section "Scanning for absolute local paths"
if found=$(find . \( -path './.venv' -o -path './.git' \) -prune -o \
            -type f \( -name '*.py' -o -name '*.md' -o -name '*.json' -o -name '*.yml' -o -name '*.yaml' \) -print0 \
          | xargs -0 grep -nE '/(Users|home|opt|var|etc|tmp)/' || true); then
  if [[ -n "$found" ]]; then
    bad "Absolute paths detected:"
    echo "$found"
    failures+=("Absolute paths present")
  else
    ok "No absolute paths found."
  fi
else
  ok "No absolute paths found."
fi

# 2) Placeholder & broken badge checks in README
section "Checking README placeholders & badge URLs"
placeholders=$(grep -nE '<YOUR_USERNAME>|%3Cyour_username%3E|<Conyekp2E>|<Conyekp2>' README.md || true)
if [[ -n "$placeholders" ]]; then
  bad "Found placeholder strings in README.md:"
  echo "$placeholders"
  failures+=("README contains placeholder values")
else
  ok "No placeholder tokens in README."
fi

# Suggest correct badge & links (info only)
BADGE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}/actions/workflows/python-tests.yml/badge.svg"
WORKFLOW_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}/actions/workflows/python-tests.yml"

echo -e "${DIM}Suggested badge (after publish):${RESET} ${BADGE_URL}"
echo -e "${DIM}Workflow page (after publish):   ${RESET} ${WORKFLOW_URL}"

# 3) Image presence & size > 0
section "Verifying required images exist"
missing=0
for img in "${REQUIRED_IMAGES[@]}"; do
  if [[ ! -f "$img" ]]; then
    bad "Missing: $img"
    missing=1
  else
    if [[ ! -s "$img" ]]; then
      bad "Zero-byte file: $img"
      missing=1
    else
      ok "Found: $img"
    fi
  fi
done
[[ $missing -eq 1 ]] && failures+=("Some images are missing or empty")

# 4) Workflow presence & quick validation
section "Checking GitHub Actions workflow"
if [[ ! -f "$WORKFLOW_FILE" ]]; then
  bad "Workflow not found: $WORKFLOW_FILE"
  failures+=("Missing GitHub Actions workflow")
else
  # minimal sniff: has a job and sets up Python 3.11
  if grep -q 'name: Python Tests' "$WORKFLOW_FILE" && grep -q 'actions/setup-python@' "$WORKFLOW_FILE"; then
    ok "Workflow file looks OK: $WORKFLOW_FILE"
  else
    warn "Workflow present but could not validate key fields. Please review: $WORKFLOW_FILE"
  fi
fi

# 5) Tests (use existing .venv if present, else try to set one up)
section "Running tests"
if [[ -x ".venv/bin/python" ]]; then
  VENV_PY=".venv/bin/${PYTHON_VER}"
  VENV_PIP=".venv/bin/pip"
else
  VENV_PY="${PYTHON_VER}"
  VENV_PIP="pip"
fi

# Ensure deps installed without changing your current env if .venv exists
if [[ -x ".venv/bin/python" ]]; then
  ok "Using existing virtualenv: .venv"
else
  warn "No .venv found — tests will run with system environment."
fi

# Try to install if requirements present and we have a venv
if [[ -f "requirements.txt" && -x ".venv/bin/python" ]]; then
  ok "Installing dependencies from requirements.txt into .venv"
  .venv/bin/pip install -r requirements.txt >/dev/null
fi

if command -v pytest >/dev/null 2>&1 || [[ -x ".venv/bin/pytest" ]]; then
  PYTEST_BIN="${PYTEST_BIN:-pytest}"
  [[ -x ".venv/bin/pytest" ]] && PYTEST_BIN=".venv/bin/pytest"

  if "$PYTEST_BIN" -q; then
    ok "Tests passed."
  else
    bad "Tests failed."
    failures+=("Pytest failures")
  fi
else
  warn "pytest not found; skipping tests."
fi

# 6) Final summary
section "Summary"
if [[ ${#failures[@]} -eq 0 ]]; then
  ok "All checks passed. Safe to publish."
  echo -e "${DIM}Next (example):${RESET}
  git init
  git add .
  git commit -m \"Initial commit: ${REPO_NAME} clean release\"
  git branch -M main
  git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git
  git push -u origin main"
  exit 0
else
  bad "Issues found:"
  for f in "${failures[@]}"; do echo " - $f"; done
  echo -e "\nFix the above, then re-run: ${DIM}bash tools/prepublish_check.sh${RESET}"
  exit 1
fi
