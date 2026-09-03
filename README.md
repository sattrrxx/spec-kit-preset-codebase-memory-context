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

Install the v1.0.2 release archive from a Spec Kit project:

```bash
specify preset add --from https://github.com/philo-x/spec-kit-preset-codebase-memory-context/archive/refs/tags/v1.0.2.zip
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

## Field Validation

The v1.0.0 release was exercised end to end against two real repositories: a
Spec Kit development checkout for the generic profile and Spring Petclinic for
the Spring Boot Maven profile. The reproducible procedure, source commits,
graph/index results, refresh check, limitations, and generated artifacts are in
[the v1.0.0 field-validation report](docs/validation/v1.0.0.md).

The [v1.0.1 MCP and workflow report](docs/validation/v1.0.1.md) additionally
verifies a real stdio MCP handshake, tool discovery, and tool call, then records
a disposable `context -> plan -> tasks -> analyze -> implement` smoke test.

CI installs `codebase-memory-mcp==0.10.8` from PyPI, verifies the executable,
and runs both CLI and stdio MCP contract tests without a skip path. A green
workflow therefore requires the supported backend and an operational MCP tool
call to be present and compatible.

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
- performs manifest-driven stack and framework detection for every project;
- probes the repository using a Universal Architecture Metamodel across 8 core
  dimensions, adapting dynamically to the discovered framework (including
  Spring Boot Maven, Go, Python/FastAPI, Node/NestJS, and polyglot setups);
- verifies graph findings against current source, build, configuration, CI,
  deployment, documentation, and representative tests;
- checks graph coverage for cited paths and bounded negative-claim scopes;
- generates compact English context across 6 focused architectural sections with
  explicit evidence and limitations; and
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
- a repository (such as Spring Boot Maven, Go, Python, or polyglot stacks)
  would benefit from framework-idiomatic API, persistence, security, testing,
  and deployment probes.

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
| `speckit.codebase-memory` | Generates or refreshes verified repository context using manifest detection and an 8-dimension Universal Architecture Metamodel. |
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
