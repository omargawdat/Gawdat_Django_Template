#!/usr/bin/env bash
set -euo pipefail

REMOTE="origin"
MERGE_PR=false

usage() {
  cat <<EOF
Usage: $0 [--merge|-m]

  --merge, -m   after creating the PR, squash-merge it, delete the branch,
                switch back to main and pull the updates
EOF
  exit 1
}

# 0. Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--merge) MERGE_PR=true; shift ;;
    -h|--help)  usage         ;;
    -*          ) echo "Unknown option: $1" >&2; usage ;;
    *           ) usage      ;;
  esac
done

# 1. Ensure we're on main
current_branch=$(git symbolic-ref --short HEAD)
if [[ "$current_branch" != "main" ]]; then
  echo "❌ Please switch to 'main' first (you’re on '$current_branch')." >&2
  exit 1
fi

# 2. Ensure no uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ Uncommitted changes detected. Please commit or stash before running." >&2
  exit 1
fi

# 3. Ensure local main isn’t behind origin/main (no fetching)
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
git push -u "$REMOTE" "$branch"

# 9. Create the PR
echo "→ Creating pull request for '$branch'…"
pr_url=$(gh pr create --base main --head "$branch" --fill)
pr_number=${pr_url##*/}
pr_number="${pr_number//[![:ascii:]]/}"
echo "→ Created PR #${pr_number}."

# 10. If --merge, squash-merge & clean up
if [[ "$MERGE_PR" == true ]]; then
  echo "→ Squash-merging PR #${pr_number} with auto-merge…"
  gh pr merge "${pr_number}" --squash --delete-branch --admin
else
  echo "→ Leaving you on feature branch '$branch'."
  git checkout "$branch"
fi
