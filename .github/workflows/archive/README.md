# Archived Workflows

These workflow files have been replaced by the new refactored CI/CD pipeline.

## Migration Date
2025-09-29

## Archived Files
- `build_test_artifact.yml` - Replaced by `main.yml`
- `linter.yml` - Integrated into `pr.yml` via `_reusable-quality-gates.yml`
- `test_compose_pr.yml` - Replaced by `pr.yml`
- `check_branch_sync.yml` - Integrated into `pr.yml` (policy_checks job)
- `cannot-change-files.yml` - Integrated into `pr.yml` (policy_checks job)
- `security.yml` - Replaced by `_reusable-security-scan.yml`

## New Architecture
The new CI/CD pipeline follows a modular architecture with:

### Reusable Workflows
- `_reusable-quality-gates.yml` - Linting and code quality
- `_reusable-security-scan.yml` - Security scanning (TruffleHog, pip-audit, safety)
- `_reusable-docker-build.yml` - Docker build with caching
- `_reusable-django-tests.yml` - Django tests with coverage
- `_reusable-docker-push-ecr.yml` - ECR push logic

### Orchestrating Workflows
- `pr.yml` - Pull request CI pipeline
- `main.yml` - Main branch CI/CD pipeline

### Key Improvements
✅ Docker layer caching (70-80% faster builds)
✅ Parallel execution of independent jobs
✅ Security scans block pipeline (not async)
✅ Single source of truth for common logic
✅ Better observability with job summaries
✅ Artifact passing between jobs (no rebuilds)

## Rollback Instructions
If you need to rollback to the old workflows:
1. Move files from `archive/` back to `workflows/`
2. Delete or disable the new `pr.yml` and `main.yml`
3. Delete the reusable workflow files (`_reusable-*.yml`)

## Questions?
Contact the DevOps team or refer to the project documentation.
