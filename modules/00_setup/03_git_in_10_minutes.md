# 03 — Git in 10 minutes for research learners

**Time:** 10–15 minutes · **Prerequisites:** Repository access and a working Git installation. This is a Markdown lesson.

Git tracks file changes, and GitHub hosts a shared copy of your project. A **commit** is a saved snapshot with a message; a **branch** isolates proposed work; a **pull request** lets others review changes before they are merged.

## Get a copy of this repository

Use GitHub Desktop's **Clone repository** command, or run:

~~~shell
git clone https://github.com/ningzhanglab/Python-for-Beginners.git
cd Python-for-Beginners
git status
~~~

This repository is currently private; you need permission to clone it. To update an existing clone, run `git pull` from your branch only after checking that you have no uncommitted conflicting changes.

## Make a focused practice branch

~~~shell
git switch -c docs/my-notes
# Edit a non-sensitive Markdown file.
git status
git add path/to/file.md
git commit -m "Document notes from introductory lesson"
~~~

Only run the `git add` step for files you actually intend to publish. Avoid private datasets, API keys, participant records, exported tables containing restricted data, and `.env` files. If you have permission to publish the branch, push it with `git push -u origin docs/my-notes` and open a pull request.

## When someone else's changes arrive

Use `git status` to check your current branch and local edits. If you are unsure, commit or safely stash your own work before pulling. Resolve conflicts by understanding both versions, not by automatically discarding one side.

## Try it (no changes to main required)

1. Run `git status` and identify which branch you are on.
2. Run `git log -3 --oneline` and explain the three newest commit messages in plain language.
3. In a **personal practice clone**, make one small documentation edit on a topic branch. Explain what a reviewer should check before accepting it.

## Common errors

- **`fatal: not a git repository`** means your shell is not inside a cloned repository directory.
- **Permission denied** during push means your GitHub account or token may not have write permission.
- **Accidentally staging large data:** use `git restore --staged path/to/file` to unstage it before committing.

## Recap

Git stores exact history; a branch keeps experimental work away from `main`; pull requests are the place for review. For scientific work, track source code and carefully licensed inputs, and recreate derived outputs through scripts.

Continue to [Module 1](../01_python_basics/README.md) and see [Git's official beginner documentation](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control).
