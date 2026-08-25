"""Tests for the Verified Codebase Context preset."""

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from packaging.version import Version
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.presets import PresetManager, PresetManifest, PresetResolver


PRESET_DIR = Path(__file__).parent.parent
CORE_OVERRIDE_COMMAND_NAMES = (
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
    "speckit.implement",
)
GENERATOR_COMMAND_NAME = "speckit.codebase-memory"
OUTPUT_TEMPLATE_NAME = "codebase-context-template"
ALL_COMMAND_NAMES = (GENERATOR_COMMAND_NAME, *CORE_OVERRIDE_COMMAND_NAMES)
CORE_MARKERS = {
    "speckit.plan": "## Mandatory Post-Execution Hooks",
    "speckit.tasks": "## Task Generation Rules",
    "speckit.analyze": "## Operating Principles",
    "speckit.implement": "## Mandatory Post-Execution Hooks",
}
COMPLETION_MARKERS = {
    "speckit.plan": "## Done When",
    "speckit.tasks": "## Done When",
    "speckit.analyze": "### 8. Offer Remediation",
    "speckit.implement": "## Done When",
}

ENV_CODEBASE_MEMORY_CLI = Path(sys.executable).with_name("codebase-memory-mcp")
CODEBASE_MEMORY_CLI = (
    str(ENV_CODEBASE_MEMORY_CLI)
    if ENV_CODEBASE_MEMORY_CLI.is_file()
    else shutil.which("codebase-memory-mcp")
)


def test_release_files_and_documentation_are_publishable():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")
    validation_report = PRESET_DIR / "docs" / "validation" / "v1.0.0.md"
    validation_artifacts = (
        PRESET_DIR
        / "docs"
        / "validation"
        / "artifacts"
    )

    assert (PRESET_DIR / "LICENSE").is_file()
    assert (PRESET_DIR / "CHANGELOG.md").is_file()
    assert validation_report.is_file()
    assert (validation_artifacts / "spec-kit-codebase.md").is_file()
    assert (validation_artifacts / "spring-petclinic-codebase.md").is_file()
    assert "## When to Use It" in readme
    assert "## When Not to Use It" in readme
    assert "docs/validation/v1.0.0.md" in readme
    assert (
        "specify preset add --from "
        "https://github.com/philo-x/spec-kit-preset-codebase-memory-context/"
        "archive/refs/tags/v1.0.0.zip"
    ) in readme
    assert "codebase-memory-mcp 0.10.8 or newer" in readme
    assert "does not require\nPyYAML" in readme

    report = validation_report.read_text(encoding="utf-8")
    assert "11,778 nodes and 58,243 edges" in report
    assert "2,076 nodes and 4,385 edges" in report
    assert "e554ba44b3fa9288ebb300d1a190e6491e85b36a3670fbb10db523c450147beb" in report


def test_installed_codebase_memory_backend_contract():
    assert CODEBASE_MEMORY_CLI is not None, (
        "codebase-memory-mcp must be installed; CI pins the supported backend "
        "in requirements-dev.txt"
    )
    version_result = subprocess.run(
        [CODEBASE_MEMORY_CLI, "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    match = re.search(r"(\d+\.\d+\.\d+)", version_result.stdout)
    assert match is not None
    assert Version(match.group(1)) >= Version("0.10.8")

    required_flags = {
        "list_projects": {"--limit", "--offset"},
        "index_repository": {"--repo-path", "--mode", "--persistence"},
        "trace_path": {"--cursor", "--include-evidence", "--limit"},
        "check_index_coverage": {
            "--paths",
            "--scopes",
            "--scope-limit",
            "--scope-offset",
        },
        "get_architecture": {"--aspects"},
    }
    for tool, flags in required_flags.items():
        help_result = subprocess.run(
            [CODEBASE_MEMORY_CLI, "cli", tool, "--help"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = help_result.stdout + help_result.stderr
        assert flags <= set(re.findall(r"--[a-z][a-z-]+", output))


def test_manifest_declares_replace_layers():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    expected_entries = {("command", name) for name in ALL_COMMAND_NAMES}
    expected_entries.add(("template", OUTPUT_TEMPLATE_NAME))

    assert manifest.id == "codebase-memory-context"
    assert manifest.version == "1.0.0"
    assert manifest.requires_speckit_version == ">=1.0.1"
    assert manifest.data["preset"]["repository"] == (
        "https://github.com/philo-x/spec-kit-preset-codebase-memory-context"
    )
    assert {
        (entry["type"], entry["name"]) for entry in manifest.templates
    } == expected_entries
    assert all(entry["strategy"] == "replace" for entry in manifest.templates)


def test_replacement_commands_are_complete_english_commands():
    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        content = command_file.read_text(encoding="utf-8")

        assert ".specify/memory/codebase.md" in content
        assert content.startswith("---\n")
        assert "scripts:" in content
        assert "## User Input" in content
        assert COMPLETION_MARKERS[command_name] in content
        assert "{CORE_TEMPLATE}" not in content
        assert "## Codebase Context Augmentation" not in content
        assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_install_resolves_replacement_without_composition(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.0.1")
    resolver = PresetResolver(project_root)

    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        layers = resolver.collect_all_layers(command_name, "command")
        assert layers[0]["strategy"] == "replace"
        assert layers[-1]["source"] == "core (bundled)"

        content = resolver.resolve_content(command_name, "command")
        assert content is not None
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        assert content == command_file.read_text(encoding="utf-8")
        assert CORE_MARKERS[command_name] in content
        assert ".specify/memory/codebase.md" in content
        assert "scripts:" in content


def test_generator_command_is_complete_and_uses_current_backend_contract():
    command_file = PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    content = command_file.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "## User Input" in content
    assert "## Done When" in content
    assert ".specify/memory/codebase.md" in content
    assert "scripts:" not in content.partition("---\n")[2].partition("---\n")[0]
    assert (
        ".specify/presets/codebase-memory-context/templates/"
        "codebase-context-template.md"
    ) in content
    assert "codebase-memory-mcp 0.10.8 or newer" in content
    assert "codebase-memory-mcp --version" in content
    assert "MCP tools" in content
    assert "codebase-memory-mcp cli --json <tool>" in content
    assert "--mode full" in content
    assert "--persistence false" in content
    assert "check_index_coverage" in content
    assert "include_evidence=true" in content
    assert "Not observed in verified scope" in content
    assert "spring-boot-maven" in content
    assert "one or two meaningful entry points" in content
    assert "stop after five representative traces" in content
    assert "PROJECT OVERRIDES START" in content
    assert "--replace-existing" in content
    assert "codegraph_explore" not in content
    assert "get_architecture(repo_path" not in content
    assert "--adopt-existing" not in content
    assert "`Executed`" not in content
    assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_generator_and_output_template_resolve_without_core_layers(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.0.1")
    resolver = PresetResolver(project_root)

    command_layers = resolver.collect_all_layers(GENERATOR_COMMAND_NAME, "command")
    assert len(command_layers) == 1
    assert command_layers[0]["strategy"] == "replace"
    assert command_layers[0]["source"] == "codebase-memory-context v1.0.0"
    assert resolver.resolve_core(GENERATOR_COMMAND_NAME, "command") is None
    assert resolver.resolve_content(GENERATOR_COMMAND_NAME, "command") == (
        PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    ).read_text(encoding="utf-8")

    template_layers = resolver.collect_all_layers(OUTPUT_TEMPLATE_NAME, "template")
    assert len(template_layers) == 1
    assert template_layers[0]["strategy"] == "replace"
    assert template_layers[0]["source"] == "codebase-memory-context v1.0.0"
    assert resolver.resolve_core(OUTPUT_TEMPLATE_NAME, "template") is None
    assert resolver.resolve_content(OUTPUT_TEMPLATE_NAME, "template") == (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")


def test_output_template_has_stable_schema_and_override_markers():
    template = (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")

    assert template.startswith("---\n")
    assert 'schema_version: "1.0"' in template
    assert 'generator: "speckit.codebase-memory"' in template
    assert 'evidence_tier: "verify"' in template
    for section_number in range(1, 15):
        assert f"## {section_number}." in template
    assert template.count("<!-- PROJECT OVERRIDES START -->") == 1
    assert template.count("<!-- PROJECT OVERRIDES END -->") == 1
    assert template.index("<!-- PROJECT OVERRIDES START -->") < template.index(
        "<!-- PROJECT OVERRIDES END -->"
    )
    assert not any("\u4e00" <= char <= "\u9fff" for char in template)


def test_codebase_rules_are_embedded_in_the_original_workflow_positions():
    plan = (PRESET_DIR / "commands" / "speckit.plan.md").read_text(encoding="utf-8")
    tasks = (PRESET_DIR / "commands" / "speckit.tasks.md").read_text(encoding="utf-8")
    implement = (PRESET_DIR / "commands" / "speckit.implement.md").read_text(
        encoding="utf-8"
    )
    analyze = (PRESET_DIR / "commands" / "speckit.analyze.md").read_text(
        encoding="utf-8"
    )

    assert plan.index(".specify/memory/codebase.md") < plan.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert plan.index("Prefer an available code graph") > plan.index(
        "### Phase 0: Outline & Research"
    )
    assert plan.index("shared model types, identifier strategies") > plan.index(
        "### Phase 1: Design & Contracts"
    )
    assert "feature-specific APIs, version compatibility" in plan
    assert "DAO or persistence registration point" not in plan
    assert "entity base classes and primary-key strategies" not in plan
    assert "controller and response-wrapper conventions" not in plan
    assert tasks.index(".specify/memory/codebase.md") < tasks.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert "repository, mapper, ORM, schema-registration" in tasks
    assert "migration, compatibility, and validation tasks" in tasks
    assert implement.index(".specify/memory/codebase.md") < implement.index(
        "4. **Project Setup Verification**"
    )
    assert "confirm it is still supported" in implement
    assert "report the substitution in the implementation summary" in implement
    assert analyze.index(".specify/memory/codebase.md") < analyze.index(
        "### 3. Build Semantic Models"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") > analyze.index(
        "### 4. Detection Passes"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") < analyze.index(
        "### 5. Severity Assignment"
    )
    assert "STRICTLY READ-ONLY" in analyze
    assert "MUST NOT exceed MEDIUM" in analyze
    assert "corroborated by current source" in analyze
    assert "Constitution conflicts remain CRITICAL" in analyze


def test_readme_documents_generator_and_context_contract():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")

    assert "one standalone generator command" in readme
    assert "`speckit.codebase-memory`" in readme
    assert "Spring Boot Maven profile" in readme
    assert "Project Overrides" in readme
    assert "`--replace-existing`" in readme
    assert "There is no\nautomatic adopt mode" in readme
    assert "does not execute them" in readme
    assert "another process to create, refresh, and maintain" not in readme
    assert "do not inherit" in readme
    assert "future core command changes" in readme
    assert "## When to Use It" in readme
    assert "## When Not to Use It" in readme
    assert "specify preset add --from" in readme
    assert "codebase-memory-mcp 0.10.8" in readme


@pytest.mark.parametrize(
    ("integration", "generator_path", "plan_path"),
    [
        (
            "codex",
            ".agents/skills/speckit-codebase-memory/SKILL.md",
            ".agents/skills/speckit-plan/SKILL.md",
        ),
        (
            "copilot",
            ".github/skills/speckit-codebase-memory/SKILL.md",
            ".github/skills/speckit-plan/SKILL.md",
        ),
        (
            "gemini",
            ".gemini/commands/speckit.codebase-memory.toml",
            ".gemini/commands/speckit.plan.toml",
        ),
    ],
)
def test_cli_init_renders_and_remove_restores_core_command(
    tmp_path, monkeypatch, integration, generator_path, plan_path
):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(
        app,
        [
            "init",
            "project",
            "--integration",
            integration,
            "--script",
            "py",
            "--preset",
            str(PRESET_DIR),
            "--ignore-agent-tools",
            "--non-interactive",
        ],
    )
    assert result.exit_code == 0, result.output

    project = tmp_path / "project"
    generator = project / generator_path
    plan = project / plan_path
    assert generator.is_file()
    assert plan.is_file()

    generator_content = generator.read_text(encoding="utf-8")
    assert (
        ".specify/presets/codebase-memory-context/templates/"
        "codebase-context-template.md"
    ) in generator_content
    assert "resolve_template.py" not in generator_content
    assert ".specify/memory/codebase.md" in plan.read_text(encoding="utf-8")

    monkeypatch.chdir(project)
    remove = CliRunner().invoke(
        app, ["preset", "remove", "codebase-memory-context"]
    )
    assert remove.exit_code == 0, remove.output
    assert not generator.exists()
    assert ".specify/memory/codebase.md" not in plan.read_text(encoding="utf-8")
