# Verified Codebase Context

Verified Codebase Context is a Spec Kit preset for established repositories. It
generates an evidence-qualified repository context at
`.specify/memory/codebase.md` and makes the core `plan`, `tasks`, `analyze`, and
`implement` workflows consume that context when it exists.

The preset provides one standalone generator command,
`speckit.codebase-memory`, one versioned output template, and four complete core
command replacements. The generator uses
[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) for graph
discovery, then requires direct repository evidence and coverage checks before
material claims are written.

## Requirements

- Spec Kit 1.0.1 or newer.
- codebase-memory-mcp 0.10.8 or newer, either configured as an MCP server or
  available as the local `codebase-memory-mcp` executable.
- A Git repository. The generator uses the canonical Git root as its safety and
  indexing boundary.

The preset does not install or update codebase-memory-mcp. It does not require
PyYAML or a project-specific helper runtime: the generator reads its installed,
preset-owned output template directly.

## Installation

Install the v1.0.0 release archive from a Spec Kit project:

```bash
specify preset add --from https://github.com/philo-x/spec-kit-preset-codebase-memory-context/archive/refs/tags/v1.0.0.zip
```

For local development:

```bash
specify preset add --dev /path/to/spec-kit-preset-codebase-memory-context
```

Verify the generator, output template, and consumer commands:

```bash
specify preset resolve speckit.codebase-memory
specify preset resolve codebase-context-template
specify preset resolve speckit.plan
specify preset resolve speckit.tasks
specify preset resolve speckit.analyze
specify preset resolve speckit.implement
```

Remove the preset with:

```bash
specify preset remove codebase-memory-context
```

## Usage

Run `speckit.codebase-memory` through the active coding agent after installing
the preset. Invoke it again whenever architecture, dependencies, deployment,
or repository conventions change materially.

The command:

- prefers the codebase-memory MCP tool surface and falls back to its local CLI;
- creates a full local graph index with `persistence=false` when needed;
- performs a generic repository analysis for every project;
- enables a deeper Spring Boot Maven profile when matching POM evidence exists;
- verifies graph findings against current source, build, configuration, CI,
  deployment, documentation, and representative tests;
- checks graph coverage for cited paths and bounded negative-claim scopes;
- generates compact English context with explicit evidence and limitations;
  and
- preserves the marked Project Overrides section on later refreshes.

The generator records repository-declared build, test, quality, run, and
deployment commands but does not execute them. It does not modify application
source, build files, configuration, tests, deployment artifacts, or any file
other than `.specify/memory/codebase.md`.

## When to Use It

Use this preset when:

- Spec Kit is being adopted in an established or unfamiliar repository;
- planning repeatedly rediscovers modules, entry points, persistence patterns,
  security boundaries, or validation commands;
- later workflow stages need a shared architecture baseline with explicit
  uncertainty and source evidence; or
- a Spring Boot Maven repository would benefit from repository-specific API,
  persistence, security, testing, and deployment probes.

## When Not to Use It

Do not use this preset when:

- codebase-memory-mcp cannot be installed or approved in the environment;
- the repository is so small or short-lived that maintaining generated context
  would cost more than rediscovery;
- runtime behavior, production traffic, or dynamic configuration must be proven
  rather than statically inferred; or
- another preset already replaces the same core commands and the two full
  replacement sets have not been reconciled.

## Context Contract

Generated files carry this ownership marker in frontmatter:

```yaml
generator: "speckit.codebase-memory"
```

The generator refreshes an owned file only when its schema and Project
Overrides markers are valid. It preserves every byte between:

```markdown
<!-- PROJECT OVERRIDES START -->
<!-- PROJECT OVERRIDES END -->
```

An existing unowned file is not overwritten by default. Move trusted manual
content into a Project Overrides section, then invoke the command with
`--replace-existing` only when a full replacement is intended. There is no
automatic adopt mode because old generated and human-authored statements cannot
be distinguished safely.

The context file is optional for the four consumer workflows. If it is absent,
each consumer follows the corresponding core workflow without codebase-context
augmentation.

## Workflow Effects

| Command | Added behavior |
|---|---|
| `speckit.codebase-memory` | Generates or refreshes verified repository context with a generic baseline and optional Spring Boot Maven profile. |
| `speckit.plan` | Uses existing architecture and conventions to fill Technical Context, focus repository discovery, limit external research, and shape data models and contracts. |
| `speckit.tasks` | Uses module and persistence conventions to anchor Setup and Foundational tasks in the existing codebase. |
| `speckit.analyze` | Optionally checks plan and task references against repository context and corroborating repository evidence. |
| `speckit.implement` | Loads coding conventions and repository-specific validation commands before executing tasks. |

## Compatibility and Maintenance

The four consumer commands use `strategy: replace`. They preserve the Spec Kit
1.0.1 command structure, script selection, native command references, and hook
surfaces, but they do not inherit future core command changes automatically.
Review and resynchronize them before each preset release that raises the
supported Spec Kit baseline.

Static graph evidence cannot prove runtime execution, production frequency,
active profiles, successful transactions, or external-service availability.
The generated context is an evidence-qualified engineering aid, not a runtime
observability report or security certification.

## License

MIT. See [LICENSE](LICENSE).
