# Changelog

All notable changes to this preset are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/philo-x/spec-kit-preset-codebase-memory-context/releases/tag/v1.0.0
