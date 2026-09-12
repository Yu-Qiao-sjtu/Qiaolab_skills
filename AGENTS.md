# Wisp Science skill requirements

All maintained skills in this repository follow Wisp Science's [authoring guide](https://github.com/xuzhougeng/wisp-science/blob/ffd8dd7af4ec80bf4fed3f3cdb878c766b970d9c/docs/skill-authoring.md) and the actual parser pinned in `validation/upstream-lock.json`. The upstream `skill-creator` instructions are the authoring reference; these repository rules record our chosen conventions.

- Keep each package at `skills/<lowercase-hyphenated-name>/SKILL.md`; explicit matching `name`, concise positive/negative trigger `description`, and closed YAML frontmatter are required here.
- Use only real controlled fields/values inside optional `wisp` metadata. Metadata never grants permission. Do not invent model, tool, runtime or automatic-loading capabilities.
- Entry bodies declare responsibilities, when to use, inputs, deliverables, exclusions, required/optional dependencies, procedure, permission boundaries and completion checks. Match task scope instead of imposing every method on every request.
- Keep detailed methods in `references/`, templates in `assets/` when needed, and executable helpers in `scripts/`. Packages must install independently: all local links remain inside the package, no symlinks, LFS pointers, external relative paths or author-machine paths.
- Install the complete folder under a project's `.wisp/skills` or use Settings → Skills for user-wide packages in `~/.wisp/skills`. Never overwrite existing user packages or write into application resources without explicit scope and a preservation plan.
- Keep private lab data and skills private. Loading a skill does not send messages, upload, execute code or install dependencies. Respect existing task authorization and host approvals; do not ask again for already-authorized actions.
- Distinguish format/package checks, temporary install tests and actual model-task validation. `verified_wisp` stays null until a named Wisp version completes a real recorded task.
- Add realistic positive, negative, missing-input, unavailable-tool and denied-action cases under `evals/`; test cases are not evidence that a model passed them.

Validation after changes:

```sh
python -X utf8 scripts/validate_skills.py
python -X utf8 -m unittest discover -s scripts -p test_packages.py -v
python -X utf8 scripts/fetch_wisp_validator.py
cargo run --locked --manifest-path validation/wisp-package-check/Cargo.toml -- skills
```

The fetch command is an explicit maintainer action with network access; skills have no runtime dependency on it. Keep the pin and content hashes together when updating upstream. Root platform adapter files are legacy exports and do not define the Wisp skill interface.
