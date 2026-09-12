# Wisp compatibility verification — 2026-09-12

Target declaration: Wisp Science **1.11.0**. Upstream parser/distribution source: `ffd8dd7af4ec80bf4fed3f3cdb878c766b970d9c`. Downloaded source hashes are recorded in `validation/upstream-lock.json` and checked before use.

## Completed locally

- 7 packages passed the original upstream `quick_validate.py`.
- 7 packages passed the unmodified upstream Rust manifest parser and distribution resource inspector.
- 7 packages installed completely into isolated temporary directories using upstream `install_new`; every installed source file matched; SKILL.md was parsed again after installation; a second installation refused to overwrite existing files.
- All package Markdown resource references passed the additional offline check, including references in supporting documents.
- 2 Python test methods passed. They check complete local installation, existing-package preservation and missing/escaping-resource failure without a partial discovered package. The private repository additionally tests its native installer wrapper.
- 7 `.skill` archives were generated using the pinned upstream packager, ZIP integrity checked, and every packaged file compared with its source.
- Local environment: Windows, Python 3.14.6, Rust 1.96.1. Validation uses no SMTP, model API, MCP service, GPU or real research data. Downloading build dependencies and upstream validation sources is an explicit maintainer step, not part of skill loading.

## CI

The `Wisp skill compatibility` workflow performs package checks, local-installer tests, upstream format/parser/installation checks and archive packaging on Windows and Linux. See the repository's Actions run for the exact commit status. The Rust validation harness is not a complete Wisp desktop build or a full `cargo test -p wisp-skills` run.

## Not performed

- No real Wisp UI session, `search_skills`/`use_skill` tool invocation or model-driven research task was run.
- Trigger and missing-capability cases in `evals/` are authored scenarios, not completed behavioral evaluations.
- Scientific validity and current accuracy of historical interview claims were not established by these format/package tests.
- No production/global skill directory was modified. GitHub store support for private repositories is not claimed.

`verified_wisp` remains null. Parser compatibility, isolated installer tests and actual model-task validation are distinct.
