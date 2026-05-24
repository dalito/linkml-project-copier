"""Tests for license template options."""

from __future__ import annotations

import sys

from copier import run_copy

from tests.helpers import DEFAULT_DATA, TEMPLATE_ROOT

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib


# Marker text expected in each LICENSE file
LICENSE_MARKERS = {
    "MIT": "The MIT License (MIT)",
    "BSD-3-Clause": "Redistribution and use in source and binary forms",
    "Apache-2.0": "Apache License",
    "MPL-2.0": "Mozilla Public License Version 2.0",
    "LGPL-3.0-only": "GNU LESSER GENERAL PUBLIC LICENSE",
    "GPL-3.0-only": "GNU GENERAL PUBLIC LICENSE",
}


class TestLicenseFile:
    """Validate LICENSE file content for each license type."""

    def test_license_marker_present(self, license_project):
        license_name, project_path = license_project
        content = (project_path / "LICENSE").read_text(encoding="utf-8")
        marker = LICENSE_MARKERS[license_name]
        assert marker in content, (
            f"LICENSE for {license_name} missing expected marker: {marker!r}"
        )

    def test_pyproject_license_field(self, license_project):
        license_name, project_path = license_project
        pyproject = tomllib.loads(
            (project_path / "pyproject.toml").read_text(encoding="utf-8")
        )
        assert pyproject["project"]["license"] == license_name


class TestApacheDefault:
    """The default license when the user accepts all defaults is Apache-2.0."""

    def test_default_is_apache(self, tmp_path):
        # Build data without a `license` key so copier falls back to the
        # question's default (Apache-2.0).
        data = {k: v for k, v in DEFAULT_DATA.items() if k != "license"}
        run_copy(
            str(TEMPLATE_ROOT),
            tmp_path,
            data=data,
            defaults=True,
            unsafe=True,
            vcs_ref="HEAD",
        )
        license_text = (tmp_path / "LICENSE").read_text(encoding="utf-8")
        assert LICENSE_MARKERS["Apache-2.0"] in license_text
        pyproject = tomllib.loads(
            (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
        )
        assert pyproject["project"]["license"] == "Apache-2.0"


class TestExistingLicenseFile:
    """When existing_license_file is set, no LICENSE is generated, the user's
    existing file is preserved, pyproject records `LicenseRef-Custom` and
    points `license-files` at the user's file."""

    def _data_with_existing(self, filename: str) -> dict:
        # Omit `license` so copier computes the dynamic default
        # ("LicenseRef-Custom" when existing_license_file is set).
        data = {k: v for k, v in DEFAULT_DATA.items() if k != "license"}
        data["existing_license_file"] = filename
        return data

    def test_no_license_generated_when_existing_file_named(self, tmp_path):
        data = self._data_with_existing("LICENSE.md")
        run_copy(
            str(TEMPLATE_ROOT),
            tmp_path,
            data=data,
            defaults=True,
            unsafe=True,
            vcs_ref="HEAD",
        )
        assert not (tmp_path / "LICENSE").exists()
        pyproject = tomllib.loads(
            (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
        )
        assert pyproject["project"]["license"] == "LicenseRef-Custom"
        assert pyproject["project"]["license-files"] == ["LICENSE.md"]

    def test_preexisting_license_md_is_preserved(self, tmp_path):
        sentinel = "MY EXISTING LICENSE — DO NOT TOUCH\n"
        (tmp_path / "LICENSE.md").write_text(sentinel, encoding="utf-8")
        data = self._data_with_existing("LICENSE.md")
        run_copy(
            str(TEMPLATE_ROOT),
            tmp_path,
            data=data,
            defaults=True,
            unsafe=True,
            vcs_ref="HEAD",
        )
        assert not (tmp_path / "LICENSE").exists()
        assert (tmp_path / "LICENSE.md").read_text(encoding="utf-8") == sentinel
