# Project records

This folder is for **optional, durable reasoning and evidence**, not a second commit history and not runtime log output. These files are project documentation: keep them under version control and never add `records/` to `.gitignore`.

## When to add a record

Write a dated record only when it would help a future maintainer understand something important that a code diff alone cannot explain: a design decision with trade-offs, a research experiment or evaluation, a major migration, a difficult bug investigation, or an important validation result.

For routine fixes or documentation polishing, a descriptive Git commit is enough. Update `CHANGELOG.md` for meaningful user-facing changes; it can link here when useful.

**Write a record for:**
- Choosing one data-cleaning method over another, and why the alternative was rejected.
- An evaluation run whose results inform what the project does next, including failed or inconclusive runs.
- A bug that took real investigation, where the root cause and the ruled-out hypotheses would save someone time later.

**Do not write a record for:**
- Fixing a typo, renaming a variable, or updating a dependency version. The commit message is enough.
- Summarizing what an agent or contributor did during a session. That belongs in the pull request description.
- Restating a diff in prose.

## Filename and scope

Use `YYYY-MM-DD-short-descriptive-topic.md` (for example, `2026-10-31-reproducibility-design.md`). Make one record per logical event. If two events occur on the same day, give them different topic slugs. Do not produce a new file for every coding step.

Start from [TEMPLATE.md](TEMPLATE.md) if it helps, but omit irrelevant sections. Prefer concise records with concrete links or evidence. Clearly separate proposed, implemented, tested, and unverified claims.

If one kind of record comes to dominate the folder (for example, many experiment runs burying a few design decisions), move that kind into a subfolder such as `records/experiments/` and keep the same filename convention there. Update links when you do.

## Changing past records

Git commits and pull requests remain authoritative for exact changes. Preserve the accuracy of past evidence and do not silently rewrite earlier findings. When a later decision or result replaces an earlier one:

1. Write a new record for the new decision or result, and link the old one under **Supersedes**.
2. In the old record, change only the **Status** to `Superseded` and add a **Superseded by** link. Leave the rest of it as written.

Use `Rejected` for a proposal that was considered and not adopted; keeping it explains why the obvious alternative was not taken.

Do not include confidential information or private research data.

## Finding records

**Indexing:** do not manually duplicate an ever-growing file list here. Use descriptive filenames, the **Type** and **Tags** lines at the top of each record, repository search, and links from `CHANGELOG.md`. For example, `grep -l "Tags:.*reproducibility" records/*.md` lists records tagged `reproducibility`.
