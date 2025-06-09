#!/usr/bin/env bash
set -euo pipefail

REMOTE="origin"
MERGE_PR=false

usage() {
  cat <<EOF
Usage: $0 [--merge|-m]
  --merge, -m   after creating (or finding) the PR, squash-merge it and clean up
EOF
  exit 1
}

# 0. Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--merge) MERGE_PR=true; shift ;;
    -* )         echo "Unknown option: $1"; usage ;;
    *  )         usage ;;
  esac
done

# 1. If on main/master, prompt for a new branch and carry over any local commits
current_branch=$(git symbolic-ref --short HEAD)
if [[ "$current_branch" =~ ^(main|master)$ ]]; then
  base_branch="$current_branch"
  echo "On '$base_branch' → creating feature branch (migrating any local commits)."
  read -rp "Enter new branch name: " branch
  while git show-ref --verify --quiet "refs/heads/$branch"; do
    echo "Branch '$branch' already exists."
    read -rp "Enter a different branch name: " branch
  done

  git fetch "$REMOTE"
  local_commits=$(git rev-list --count "$REMOTE/$base_branch"..HEAD)

  if (( local_commits > 0 )); then
    echo "→ You have $local_commits local commit(s). Spinning them off onto '$branch'."
    git checkout -b "$branch"
    git checkout "$base_branch"
    git reset --hard "$REMOTE/$base_branch"
    git checkout "$branch"
  else
    git checkout -b "$branch" "$REMOTE/$base_branch"
  fi
else
  branch="$current_branch"
  echo "Working on existing branch '$branch'."
fi

# 2. Commit any unstaged changes
if ! git diff-index --quiet HEAD --; then
  echo "→ Uncommitted changes detected."
  read -rp "Commit message: " msg
  git add --all
  git commit -m "$msg"
else
  echo "→ No changes to commit."
fi

# 3. Push branch
git push -u "$REMOTE" "$branch"

# 4. Check for GitHub CLI
if ! command -v gh &>/dev/null; then
  echo "⚠️  GitHub CLI ('gh') not found. Install it to automate PR creation/merging."
  exit 1
fi

# 5. Detect or create PR
if pr_number=$(gh pr view "$branch" --json number --jq .number 2>/dev/null); then
  echo "→ Found existing PR #$pr_number for '$branch'."
  gh pr view --web
  read -rp "Open that PR in browser and exit? (y/N) " yn
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    exit 0
  fi
else
  pr_out=$(gh pr create --base main --head "$branch" --fill)
  pr_url=$(echo "$pr_out" | tail -n1)
  pr_number=${pr_url##*/}
  echo "→ Created PR #$pr_number."
fi

# 6. Optionally squash-merge, delete branches, and update main
if [[ "$MERGE_PR" == true ]]; then
  echo "→ Squash-merging PR #$pr_number…"
  if gh pr merge "$pr_number" --squash; then
    echo "→ PR #$pr_number squash-merged successfully."

    # Switch back to main
    echo "→ Checking out 'main'…"
    git checkout main

    # Delete the feature branch locally
    echo "→ Deleting local branch '$branch'…"
    git branch -d "$branch"

    # Delete the feature branch remotely
    echo "→ Deleting remote branch '$branch'…"
    git push "$REMOTE" --delete "$branch"

    # Pull the updated main
    echo "→ Pulling latest 'main' from '$REMOTE'…"
    git pull "$REMOTE" main

    echo "→ Local 'main' is now up-to-date with the squash-merge."
  else
    echo "❌ Failed to squash-merge PR #$pr_number."
    exit 1
  fi
fi
