"""Tests for license template options."""

from __future__ import annotations

import tomllib


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
