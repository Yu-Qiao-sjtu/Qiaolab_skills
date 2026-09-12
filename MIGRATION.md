# Consolidation — 2026-09-12

- Qiaolab_skills base: `c73e49ec44f16229c459c3bcdf4c827a0f3dcc50`. AI4asking gains discoverable frontmatter and normalized directory naming.
- Wisp_skills: `478e062e6fba57df825be5d628980e64e12ad7e1`. Five complete skill directories copied with their references unchanged. License retained as `LICENSE-Wisp_skills`; upstream cangjie-skill and Wisp Science attribution remains in the skill content and source history.
- Pro.-Paper: `822d3985f0de10e5a95e9ccc328880096d08ed35`. System framework and all eight module instructions retained under `skills/paper-deconstruction/references/`. A scoped entrypoint replaces the standalone UI for agent use; PDF parsing and HTML export code remain in the archived source application.
- Private qianlab-notebook-skill is not imported into this public repository.

The source histories remain in archived repositories. Install individual complete directories from `skills/`. This migration does not modify global agent configuration.

## Wisp authoring alignment

Following consolidation, all seven active packages were adapted to the pinned Wisp Science authoring guide. Long original methods and source notes moved into package-local references; obsolete single-file installation instructions were replaced. Source snapshots are no longer byte-identical after this adaptation; the original revision references above remain available in Git history. See docs/WISP-STANDARD.md and docs/VALIDATION.md.
