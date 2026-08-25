---
schema_version: "1.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - generic
source_commit: "b0b02cf1d6944279aaaa66223374c86e38c2565e"
working_tree: "modified only by preset installation"
evidence_tier: "verify"
---

# GitHub Spec Kit Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. System Purpose

Spec Kit provides a spec-driven development workflow and the `specify` CLI that
initializes repositories, installs coding-agent integrations, and manages
workflows, extensions, and presets. Its primary users are software teams and
AI coding agents that consume the installed Markdown skills or commands.

## 2. Technology Inventory

| Layer | Technology | Version / Detail | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| Runtime | Python | 3.11 or newer | Wired | Verified | `pyproject.toml` |
| CLI | Typer and Click | Typer >=0.24.0, Click >=8.2.1 | Wired | Verified | `pyproject.toml`, `src/specify_cli/__init__.py` |
| Configuration | YAML, JSON, JSON5 | PyYAML >=6.0; project registries and manifests | Wired | Verified | `pyproject.toml`, `src/specify_cli/presets/__init__.py` |
| Packaging | Hatchling | wheel includes core templates, scripts, workflows, extensions, and presets | Wired | Verified | `pyproject.toml` |
| Tests | pytest, pytest-cov | pytest >=7.0 | Wired | Verified | `pyproject.toml`, `tests/` |

## 3. Module and Package Map

### Module Tree

- `src/specify_cli/`: CLI entry point and lifecycle managers.
- `src/specify_cli/integrations/`: agent-specific command/skill materialization.
- `src/specify_cli/presets/`: preset manifests, installation, registry, and
  layered resolution.
- `src/specify_cli/extensions/`: extension lifecycle, hooks, and command
  registration.
- `src/specify_cli/workflows/`: bundled workflow catalog and engine.
- `templates/`, `scripts/`, `workflows/`, `extensions/`, `presets/`: source
  assets embedded into the distribution.
- `tests/`: unit, contract, integration, workflow, hook, and security tests.

### Dependency Direction

The `specify` command dispatches into workflow and lifecycle managers. Preset
installation validates a manifest, copies an isolated preset, updates the
project registry, and registers commands through the integration layer.
Resolution reads project overrides, enabled presets and extensions by priority,
then bundled core assets. This direction is corroborated by direct source and
graph traces from `PresetManager.install_from_directory` and
`PresetResolver.resolve_content`.

### Package Conventions

Python packages live below `src/specify_cli`; distributable non-Python assets
remain in their top-level source directories and are mapped into
`specify_cli/core_pack` by Hatchling. Tests mirror the affected subsystem and
use `test_*.py` names.

### Entry Points

- `specify = specify_cli:main` is the public CLI entry point.
- Standalone Python helpers in `scripts/python/` implement feature, plan, task,
  and prerequisite workflows.
- Bundled extension helpers under `extensions/*/scripts/python/` are invoked by
  their extension commands.

## 4. Request, Messaging, Job, and Data Flows

### Global Request and Exception Pipeline

There is no server request pipeline. Typer parses a CLI invocation, dispatches
to the relevant manager or workflow step, and Rich renders progress and errors.

### Representative Traces

1. Preset installation: CLI preset command -> archive/directory validation ->
   `PresetManager.install_from_directory` -> compatibility and path checks ->
   registry update -> command/skill reconciliation. The graph returned 108
   outbound callees across two cursor pages; direct source was used to filter
   heuristic noise.
2. Template resolution: caller -> `PresetResolver.resolve_content` ->
   `collect_all_layers` -> project/preset/extension/core lookup -> strategy
   composition -> resolved text. The verified trace returned 29 callees.
3. Project initialization: `specify init` -> workflow steps -> integration
   setup -> bundled shared infrastructure and workflow installation.

## 5. Persistence Model and Transaction Boundaries

The project has no application database. Installed state is file-backed below
`.specify`, including preset and extension registries and copied artifacts.
Lifecycle operations use validation, temporary extraction, and controlled file
writes; they are not database transactions and process interruption can only be
reasoned about from the individual implementation paths.

## 6. Integration Points

| Integration | Mechanism | Consumer | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| Coding agents | Generated commands or skills | Integration registry | Wired | Verified | `src/specify_cli/integrations/` |
| Community presets | HTTPS release archive or catalog metadata | Preset manager | Wired | Verified | `src/specify_cli/presets/__init__.py`, `README.md` |
| Community extensions | Bundled, local, or trusted HTTPS source | Extension manager | Wired | Verified | `src/specify_cli/extensions/__init__.py` |
| PyPI/GitHub releases | Package and release workflows | End users | Configured-only | Verified | `pyproject.toml`, `.github/workflows/publish-pypi.yml` |

## 7. Security Model

This is a local developer tool, not an authenticated service. Trust boundaries
are downloaded archives, local paths, symlinks, agent output directories, and
subprocess invocation. Preset tests cover malformed manifests, unsafe symlinks,
archive extraction, compatibility checks, and priority resolution. No claim is
made that these static checks prove all supply-chain or runtime threats absent.

## 8. Testing Strategy

pytest discovers `tests/test_*.py` with strict markers and verbose short
tracebacks. Tests are divided among focused subsystem files plus contract,
integration, workflow, hook, and security suites. `tests/test_presets.py`
exercises manifest validation, install/remove, archive safety, registry
priority, and resolver composition. CI runs the repository test suite on the
supported Python matrix.

## 9. Coding and Repository Modification Conventions

Use the repository virtual environment for tests. Keep integration metadata in
the integration registry, track installed files through manifests, and preserve
all supported script variants when a shared workflow contract changes. New
Python code belongs under `src/specify_cli`; tests belong in the matching
`tests/test_*.py` subsystem file.

## 10. Operational Constraints and Automation

Python >=3.11 is required. Core initialization is designed to work from bundled
assets without a network connection, while remote preset/extension installation
requires explicitly trusted HTTPS sources where applicable. GitHub Actions
contains test, lint, security, documentation, and release workflows.

## 11. Known Risks and Technical Debt

| Finding | Impact | Confidence | Evidence | Recommendation |
|---|---|---|---|---|
| Preset `replace` layers do not inherit later core edits | Community replacements can drift from core commands | Verified | preset resolution behavior and preset publishing guidance | Rebase complete replacements on each supported Spec Kit baseline |
| Four shell/PowerShell files have partial parse ranges | Graph-only shell conclusions may miss constructs | Verified | `index_status` generation `2026-08-25T23:28:01Z` | Read the reported ranges directly before claims about those scripts |
| Remote archives are a supply-chain boundary | A trusted URL can still deliver unwanted content | Verified | preset/extension installation paths | Pin release tags and retain archive/path validation tests |

## 12. Build, Test, Quality, and Run Commands

| Purpose | Command | Preconditions | Evidence |
|---|---|---|---|
| Install development dependencies | `uv sync --extra test` | uv and Python >=3.11 | `AGENTS.md`, `pyproject.toml` |
| Run tests | `.venv/bin/python -m pytest` | repository virtualenv synchronized | `AGENTS.md`, `pyproject.toml` |
| Run CLI | `.venv/bin/specify --help` | repository virtualenv synchronized | `pyproject.toml` |
| Initialize a project | `.venv/bin/specify init my-project --integration codex` | selected agent integration | `README.md` |

## 13. Evidence and Coverage Limitations

The fresh, non-persistent full index was
`private-tmp-spec-kit-field-validation-spec-kit`, status `ready`, with 11,778
nodes and 58,243 edges. Exact checks for `pyproject.toml`, `README.md`,
`src/specify_cli/presets/__init__.py`, `tests/test_presets.py`, and
`.github/workflows/test.yml`, plus the bounded `src/specify_cli/presets` scope,
reported no recorded issue with matching generation metadata. This is a
best-effort signal, not completeness proof. Four reported partial parser ranges
in Bash/PowerShell files were outside material claims here; non-code manifests,
documentation, and CI were read directly. No build or test command was executed
by the generator, and release service behavior remains statically inferred.

<!-- PROJECT OVERRIDES START -->
## 14. Project Overrides

> Human-maintained and preserved verbatim. The generator does not validate this
> section or use it to raise the confidence of generated findings.

<!-- PROJECT OVERRIDES END -->
