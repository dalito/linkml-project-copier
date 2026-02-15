"""Fixtures and helpers for linkml-project-copier template tests."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent

ALL_LICENSES = ["MIT", "BSD-3-Clause", "Apache-2.0", "MPL-2.0", "LGPL-3.0-only", "GPL-3.0-only"]

DEFAULT_DATA = {
    "project_name": "test-schema",
    "project_slug": "test_schema",
    "email": "test@example.org",
    "full_name": "Test User",
    "github_org": "test-org",
    "project_description": "A test project.",
    "license": "MIT",
    "copyright_year": "2025",
    "add_example": True,
    "gh_action_pypi": True,
    "gh_action_docs_preview": True,
}


def generate_project(
    dest: Path,
    data_overrides: dict | None = None,
) -> Path:
    """Generate a project from the copier template.

    Args:
        dest: Directory where the project will be generated.
        data_overrides: Values to override in DEFAULT_DATA.

    Returns:
        Path to the generated project directory.
    """
    data = {**DEFAULT_DATA, **(data_overrides or {})}
    run_copy(
        str(TEMPLATE_ROOT),
        dest,
        data=data,
        defaults=True,
        unsafe=True,
        vcs_ref="HEAD",
    )
    return dest


def git_init(project_dir: Path) -> None:
    """Initialize a git repo with an initial commit (needed for dynamic versioning)."""
    subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=project_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=project_dir,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=project_dir,
        check=True,
        capture_output=True,
    )


def run_just(project_dir: Path, *args: str, timeout: int = 600) -> subprocess.CompletedProcess:
    """Run a just command in the given project directory."""
    return subprocess.run(
        ["just", *args],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# Session-scoped fixtures for structural tests (read-only, generated once)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def default_project(tmp_path_factory):
    """Project generated with all defaults and add_example=True."""
    dest = tmp_path_factory.mktemp("default")
    return generate_project(dest)


@pytest.fixture(scope="session")
def no_example_project(tmp_path_factory):
    """Project generated with add_example=False."""
    dest = tmp_path_factory.mktemp("no_example")
    return generate_project(dest, {"add_example": False})


@pytest.fixture(scope="session")
def no_pypi_project(tmp_path_factory):
    """Project generated with gh_action_pypi=False."""
    dest = tmp_path_factory.mktemp("no_pypi")
    return generate_project(dest, {"gh_action_pypi": False})


@pytest.fixture(scope="session")
def no_docs_preview_project(tmp_path_factory):
    """Project generated with gh_action_docs_preview=False."""
    dest = tmp_path_factory.mktemp("no_docs_preview")
    return generate_project(dest, {"gh_action_docs_preview": False})


@pytest.fixture(scope="session", params=ALL_LICENSES)
def license_project(request, tmp_path_factory):
    """Project generated for each license type. Returns (license_name, project_path)."""
    license_name = request.param
    dest = tmp_path_factory.mktemp(f"license_{license_name}")
    project_path = generate_project(dest, {"license": license_name})
    return license_name, project_path
