#!/usr/bin/env bash
set -euo pipefail

REMOTE="origin"
NO_VERIFY=false

usage() {
  cat <<EOF
Usage: $0 [--no-verify]

  --no-verify     skip pre-push hooks validation
EOF
  exit 1
}

# 0. Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-verify)    NO_VERIFY=true; shift ;;
    -h|--help)      usage         ;;
    -*              ) echo "Unknown option: $1" >&2; usage ;;
    *               ) usage      ;;
  esac
done

# 1. Detect current branch and determine flow
current_branch=$(git symbolic-ref --short HEAD)
ON_MAIN=false
if [[ "$current_branch" == "main" ]]; then
  ON_MAIN=true
fi

# 2. Ensure no uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ Uncommitted changes detected. Please commit or stash before running." >&2
  exit 1
fi

# ============================================================================
# FEATURE BRANCH FLOW: If on a feature branch, push and create PR
# ============================================================================
if [[ "$ON_MAIN" == false ]]; then
  echo "→ On feature branch '$current_branch'. Pushing and creating PR…"

  # Run pre-push validation if needed
  if [[ "$NO_VERIFY" == false ]]; then
    echo "→ Running pre-push validation…"
    if ! git push --dry-run "$REMOTE" "$current_branch" 2>/dev/null; then
      echo "❌ Pre-push validation failed. Please fix the issues and try again." >&2
      exit 1
    fi
    echo "✓ Pre-push validation passed."
  fi

  # Push the feature branch
  echo "→ Pushing '$current_branch' to '$REMOTE'…"
  if [[ "$NO_VERIFY" == true ]]; then
    git push --no-verify -u "$REMOTE" "$current_branch"
  else
    git push -u "$REMOTE" "$current_branch"
  fi

  # Create the PR
  echo "→ Creating pull request for '$current_branch'…"
  pr_url=$(gh pr create --base main --head "$current_branch" --fill)
  pr_number=${pr_url##*/}
  pr_number="${pr_number//[![:ascii:]]/}"
  echo "→ Created PR #${pr_number}."

  # Open PR in browser
  echo "→ Opening PR in browser…"
  gh pr view "${pr_number}" --web

  exit 0
fi

# ============================================================================
# MAIN BRANCH FLOW: Create new branch, move commits, create PR
# ============================================================================

# 3. Ensure local main isn't behind origin/main (no fetching)
behind_count=$(git rev-list --count main.."$REMOTE"/main)
if (( behind_count > 0 )); then
  echo "❌ Your local 'main' is behind '$REMOTE/main' by $behind_count commit(s)."
  echo "   Please pull the latest changes and re-run."
  exit 1
fi

# 4. Count how many commits on main need moving
ahead_count=$(git rev-list --count "$REMOTE"/main..main)
if (( ahead_count == 0 )); then
  echo "→ No local commits on 'main' to move; nothing to do."
  exit 0
fi
echo "→ Found $ahead_count local commit(s) on 'main'."

# 4.5. Run pre-push validation early (before any destructive operations)
if [[ "$NO_VERIFY" == false ]]; then
  echo "→ Running pre-push validation…"
  if ! git push --dry-run "$REMOTE" main 2>/dev/null; then
    echo "❌ Pre-push validation failed. Please fix the issues and try again." >&2
    exit 1
  fi
  echo "✓ Pre-push validation passed."
fi

# 5. Prompt for a new branch name
read -rp "Enter new branch name: " branch
while git show-ref --verify --quiet "refs/heads/$branch"; do
  echo "Branch '$branch' already exists."
  read -rp "Enter a different branch name: " branch
done

# 6. Create the feature branch with your commits
echo "→ Creating branch '$branch' with your commits…"
git checkout -b "$branch"

# 7. Reset main back to origin/main
echo "→ Resetting 'main' to match '$REMOTE/main'…"
git checkout main
git reset --hard "$REMOTE/main"

# 8. Push the feature branch
echo "→ Pushing '$branch' to '$REMOTE'…"
git checkout "$branch"
if [[ "$NO_VERIFY" == true ]]; then
  git push --no-verify -u "$REMOTE" "$branch"
else
  git push -u "$REMOTE" "$branch"
fi

# 9. Create the PR
echo "→ Creating pull request for '$branch'…"
pr_url=$(gh pr create --base main --head "$branch" --fill)
pr_number=${pr_url##*/}
pr_number="${pr_number//[![:ascii:]]/}"
echo "→ Created PR #${pr_number}."

# 10. Open PR in browser
echo "→ Opening PR in browser…"
gh pr view "${pr_number}" --web
