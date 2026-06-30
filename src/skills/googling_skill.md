---
ID: googling
NAME: Effective Googling
DESCRIPTION: Search the web, official docs, forums, databases, and error messages with precise query operators and source-quality checks.
VERSION: 1.0
TAGS: google, search, documentation, database, research, debugging
---

# Effective Googling Skill

Use this skill when the user needs to find accurate information, debug an error, locate documentation, compare sources, or search a specific website or database.

## Core Search Flow

1. Restate the target in plain words.
2. Identify exact terms: product name, library name, error text, file name, function name, version, platform, or database engine.
3. Start broad, then add constraints only when results are noisy.
4. Prefer primary sources first: official docs, release notes, source repos, standards, vendor docs, issue trackers.
5. Cross-check claims from blogs, forums, and AI-generated pages against official sources.
6. Save the best query pattern if it works, then reuse it with one variable changed.

## High-Value Google Operators

- `"exact phrase"`: search exact text, useful for error messages and API names.
- `site:example.com`: search inside one site.
- `-term`: exclude noisy results.
- `OR`: search alternatives, such as `postgres OR postgresql`.
- `filetype:pdf`: find PDFs, specs, manuals, and reports.
- `intitle:term`: require a word in the page title.
- `inurl:term`: require a word in the URL.
- `after:YYYY-MM-DD`: prefer newer results.
- `before:YYYY-MM-DD`: find older behavior or removed docs.
- `*`: wildcard inside exact phrases.

## Documentation Search Patterns

Use official docs when possible:

```text
site:docs.python.org pathlib read_text encoding
site:react.dev useEffect cleanup
site:docs.djangoproject.com migrations RunPython examples
site:docs.sqlalchemy.org session rollback exception
```

Find version-specific docs:

```text
site:docs.python.org/3.12 pathlib Path.is_relative_to
site:postgresql.org/docs/15 jsonb index
site:dev.mysql.com/doc/refman/8.0 generated columns
```

Find changelogs or breaking changes:

```text
site:github.com/project/repo releases breaking change keyword
site:github.com/project/repo/issues exact error message
site:project.org changelog "feature name"
```

## Error Debugging Patterns

Search the most specific stable part of an error:

```text
"TypeError: object is not subscriptable" library_name
"ModuleNotFoundError: No module named" package_name python version
"relation does not exist" postgresql schema search_path
```

Remove local paths, timestamps, IDs, tokens, usernames, and machine-specific values before searching.

When results are noisy, add:

```text
site:github.com
site:stackoverflow.com
site:docs.vendor.com
-"AI overview"
```

## Database Search Tricks

For SQL/database work, include the engine and version because behavior differs:

```text
postgresql 16 upsert on conflict partial index
mysql 8.0 window function running total
sqlite generated columns limitations
sql server 2022 deadlock graph xml
mongodb aggregation lookup pipeline examples
```

Search official database docs:

```text
site:postgresql.org/docs "CREATE INDEX" gin jsonb
site:dev.mysql.com/doc/refman "EXPLAIN ANALYZE"
site:sqlite.org "without rowid"
site:learn.microsoft.com sql server isolation levels
site:mongodb.com/docs aggregation stage unwind
```

Search query plans and performance:

```text
postgresql slow query explain analyze nested loop
mysql composite index order by where
sqlite query planner covering index
mongodb explain executionStats slow query
```

Search migrations and ORM behavior:

```text
site:docs.sqlalchemy.org alembic add column nullable default
site:docs.djangoproject.com migration RunSQL reverse_sql
site:guides.rubyonrails.org active record migration index concurrently
site:prisma.io/docs migrate existing database
```

## Research Quality Checks

Trust sources in this rough order:

1. Official documentation, specifications, release notes, and source code.
2. Maintainer comments in issues, pull requests, and discussions.
3. Well-known technical blogs with reproducible examples.
4. Q&A/forum answers with dates, versions, accepted fixes, and comments.
5. Unsourced summaries only as leads, not final authority.

Always check publication date for fast-moving topics like cloud services, libraries, pricing, security, and API behavior.

## Query Refinement

If results are too broad:

```text
"exact function name" "exact error phrase" library_name
site:official-docs-domain.com exact term
keyword keyword -beginner -tutorial
```

If results are too narrow:

```text
remove version
replace exact phrase with key terms
replace framework-specific term with generic term
try synonyms OR alternatives
```

If searching docs fails:

```text
site:github.com org repo keyword
site:github.com org repo/issues keyword
site:github.com org repo/discussions keyword
```

## Useful Templates

```text
site:official-docs-domain.com product feature exact_term
"exact error message" product version platform
product version "breaking changes" feature
product "migration guide" old_version new_version
database version query_feature performance
site:github.com owner repo issue_keyword error_keyword
filetype:pdf standard_or_protocol_name version
```

## When To Stop Searching

Stop when you have:

- A primary source that directly answers the question.
- A reproducible fix or command from an official doc or maintainer.
- Two independent reliable sources agreeing on behavior.
- A clear note that the behavior depends on version, platform, or configuration.

If evidence conflicts, report the conflict and cite the source dates, versions, or environments that explain the difference.
