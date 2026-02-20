# Branch Protection Setup Guide

This document describes the manual steps to configure branch protection rules in GitHub.

## Prerequisites

- The `.github/workflows/tests.yml` workflow must be pushed to the repository
- At least one pull request must have run the workflow to generate status checks

## Steps

1. Navigate to your repository on GitHub
2. Click **Settings** tab
3. In the left sidebar, click **Branches**
4. Click **Add branch protection rule**
5. Enter `main` as the branch name pattern
6. Configure the following settings:

### Required Settings

✅ **Require status checks to pass before merging**
- Enable this checkbox
- In the "Required status checks" search box, select:
  - `test (3.8)`
  - `test (3.9)`
  - `test (3.10)`
  - `test (3.11)`
  - `test (3.12)`

✅ **Require branches to be up to date before merging**
- Enable this checkbox

### Optional Settings (Recommended)

🔹 **Require pull request reviews before merging**
- Set required approvers to 1 (or your team's requirement)

🔹 **Do not allow bypassing the above settings**
- Enable for stricter control

7. Click **Create** or **Save changes**

## Verification

After setup, create a test pull request:
1. Create a branch from main
2. Make a trivial change (e.g., update a comment)
3. Push and create a PR
4. Verify that:
   - GitHub Actions runs 5 test jobs (one per Python version)
   - All jobs must pass before the merge button becomes enabled
   - If you break a test, the merge button is disabled

## Troubleshooting

**Status checks not appearing:**
- Ensure the workflow has run at least once on a PR
- Check that the workflow name and job name match exactly
- Refresh the branch protection page

**Merge button still enabled when tests fail:**
- Double-check that all 5 test status checks are selected in the branch protection rule
- Ensure "Require status checks to pass before merging" is enabled
