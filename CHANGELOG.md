# Changelog

All notable changes to this preset are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-09-03

### Changed

- Bumped document contract to **`schema_version: "2.0"`**, with backwards-compatible upgrade handling for owned 1.0 documents during refresh.
- Replaced the hardcoded Spring Boot Maven probe with a **Universal Architecture Metamodel** across 8 core dimensions and an **Idiomatic Self-Introspection Protocol**, supporting full probing for the primary stack and targeted boundary/command probing for secondary polyglot stacks (e.g., frontend SPA, CLI, workers).
- Streamlined `codebase-context-template.md` from 14 sections down to a focused 6-section structure (Architecture & Module Map, Core Flows & Boundaries with dedicated Security slot, Data Persistence, Development Conventions with Operational/Packaging slot & Deploy commands, Evidence Limitations, Project Overrides), reducing token consumption and improving agent compliance.
- Updated generator word budget to 1,200 - 2,500 words (ceiling 3,500 words).
- Updated automated preset tests in `test_preset.py` to assert the schema 2.0 template and metamodel protocol.

## [1.0.1] - 2026-08-26

### Added

- Reproducible v1.0.0 field-validation report and generated context artifacts
  for a generic Python project and a Spring Boot Maven project.
- MCP stdio contract validation covering initialization, tool discovery, and a
  real read-only tool call.
- End-to-end downstream workflow evidence covering context generation, plan,
  tasks, analysis, implementation, and project tests.

### Changed

- CI now installs `codebase-memory-mcp==0.10.8` and fails when the backend
  executable, required CLI contract, or MCP stdio contract is unavailable.

## [1.0.0] - 2026-08-26

### Added

- `speckit.codebase-memory` generator for evidence-qualified repository context.
- Stable `.specify/memory/codebase.md` schema with ownership and preserved
  Project Overrides markers.
- Generic repository analysis and an evidence-triggered Spring Boot Maven
  profile.
- codebase-memory-mcp graph discovery, representative traces, direct-source
  corroboration, and index-coverage auditing.
- Repository-aware replacements for `speckit.plan`, `speckit.tasks`,
  `speckit.analyze`, and `speckit.implement`.
- Installation and rendering coverage for skills-based and command-based agent
  integrations.

[Unreleased]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/releases/tag/v1.0.0
