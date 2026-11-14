---
name: changelog-automation
description: keep a changelog ve semver standartlarinda commit ve pr gecmisinden otomatik degisiklik gunlugu uretimi.
when_to_use: "surum yayinlama (release), versiyonlama ve kurumsal surum notlari hazirlanirken kullanilir."
allowed-tools: Read, Write, Edit, Grep
version: 1.0.0
---

# changelog-automation — kurumsal standartlar ve uygulama rehberi

> 46 p0 kuralina ve sifir varsayim ilkesine bagli kurumsal operasyon kalibi.

# Changelog Automation

Patterns and tools for automating changelog generation, release notes, and version management following industry standards.

## Use this skill when

- Setting up automated changelog generation
- Implementing conventional commits
- Creating release note workflows
- Standardizing commit message formats
- Managing semantic versioning

## Do not use this skill when

- The project has no release process or versioning
- You only need a one-time manual release note
- Commit history is unavailable or unreliable

## Instructions

- Select a changelog format and versioning strategy.
- Enforce commit conventions or labeling rules.
- Configure tooling to generate and publish notes.
- Review output for accuracy, completeness, and wording.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Safety

- Avoid exposing secrets or internal-only details in release notes.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, templates, and examples.
