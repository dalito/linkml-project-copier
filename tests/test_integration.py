"""Integration tests that run just commands in generated projects."""

from __future__ import annotations

import pytest

from conftest import generate_project, git_init, run_just

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def integration_project(tmp_path_factory):
    """Generate a project with git init for integration testing (mutable)."""
    dest = tmp_path_factory.mktemp("integration")
    project = generate_project(dest)
    git_init(project)
    return project


def test_just_install(integration_project):
    result = run_just(integration_project, "install")
    assert result.returncode == 0, (
        f"just install failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_just_test(integration_project):
    result = run_just(integration_project, "test")
    assert result.returncode == 0, (
        f"just test failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_just_lint(integration_project):
    result = run_just(integration_project, "lint")
    assert result.returncode == 0, (
        f"just lint failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_just_gen_doc(integration_project):
    result = run_just(integration_project, "gen-doc")
    assert result.returncode == 0, (
        f"just gen-doc failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
