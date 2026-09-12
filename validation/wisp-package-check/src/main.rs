#![allow(dead_code, unused_imports)]
// AGPL-3.0-only. Executes the commit-pinned upstream parser and package installer
// in temporary directories only; never installs to a user's Wisp configuration.
extern crate self as wisp_dto;
#[path = "../../../.wisp-upstream/crates/wisp-dto/src/lib.rs"]
mod upstream_dto;
pub use upstream_dto::*;
#[path = "../../../.wisp-upstream/crates/wisp-skills/src/manifest.rs"]
mod manifest;
#[path = "../../../.wisp-upstream/crates/wisp-skills/src/distribution.rs"]
mod distribution;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let skills = std::env::args().nth(1).unwrap_or_else(|| "skills".into());
    let root = std::fs::canonicalize(&skills)?;
    // Synthetic provenance for a local fixture: not a claim that these bytes
    // were downloaded from GitHub or installed in a real Wisp user account.
    let source = SkillInstallSource {
        repository: "fixtures/skills".into(),
        source_url: "https://github.com/fixtures/skills".into(),
        git_ref: "local-fixture".into(),
        commit: "0".repeat(40),
        package_path: String::new(),
    };
    let candidates = distribution::inspect_repository(&root, &source)?;
    let temporary = tempfile::tempdir()?;
    let installed_root = temporary.path().join("skills");
    for candidate in &candidates {
        assert!(candidate.format_errors.is_empty(), "{}: {:?}", candidate.name, candidate.format_errors);
        assert!(candidate.resource_errors.is_empty(), "{}: {:?}", candidate.name, candidate.resource_errors);
        let installed = distribution::install_new(&root, &installed_root, candidate)?;
        let md = std::fs::read_to_string(installed.join("SKILL.md"))?;
        let (parsed, body) = manifest::parse_skill_document(&md, candidate.name.clone())?;
        assert_eq!(parsed.name.as_deref(), Some(candidate.name.as_str()));
        assert!(!body.is_empty());
        for entry in walkdir::WalkDir::new(root.join(&candidate.source.package_path)) {
            let entry = entry?;
            if entry.file_type().is_file() {
                let base = root.join(&candidate.source.package_path);
                let relative = entry.path().strip_prefix(&base)?;
                assert_eq!(std::fs::read(entry.path())?, std::fs::read(installed.join(relative))?);
            }
        }
        // The real installer must preserve an already installed package.
        assert!(distribution::install_new(&root, &installed_root, candidate).is_err());
        assert_eq!(std::fs::read_to_string(installed.join("SKILL.md"))?, md);
        println!("PASS {}: upstream parse, resource inspection, isolated install, reload, no-overwrite", candidate.name);
    }
    let repo = root.parent().ok_or("skills directory has no parent")?;
    if repo.join("community-skills/index.json").is_file() {
        let entries = distribution::parse_catalog(&std::fs::read(repo.join("community-skills/index.json"))?)?;
        assert_eq!(entries.len(), candidates.len());
        for entry in &entries {
            let skill = candidates.iter().find(|candidate| candidate.name == entry.name).ok_or("catalog name mismatch")?;
            assert_eq!(entry.description, skill.description);
            assert!(entry.verified_wisp.is_none(), "model runtime validation has not been performed");
        }
        println!("PASS upstream community catalog: {} entries", entries.len());
    }
    println!("Validated {} packages. No model task, network service or production installation was executed.", candidates.len());
    Ok(())
}
