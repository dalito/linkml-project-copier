# Contributing to linkml-project-copier

Thank you for considering a contribution!

## Prerequisites

- **Python >= 3.10**
- **uv** -- for dependency management and running tests
- **just** -- only needed if you want to run integration tests locally
  (`uv tool install rust-just`)

## Getting started

```shell
git clone https://github.com/linkml/linkml-project-copier.git
cd linkml-project-copier
uv sync --group test
```

## Running the tests

The test suite has two tiers:

```shell
# Structural tests only (fast, ~25 seconds, no just/linkml needed)
uv run pytest -m "not integration" -v

# Integration tests only (slow, minutes, needs just + network)
uv run pytest -m integration -v

# Everything
uv run pytest -v
```

### Important: commit before testing

The tests use copier's Python API with `vcs_ref="HEAD"`, which means copier
generates projects from the **last commit** on the current branch. If you
modify template files without committing, the tests will run against the
old commit and your changes won't be covered.

## Test architecture

### Two tiers

**Structural tests** (`test_generation.py`, `test_options.py`,
`test_licenses.py`) generate projects via copier's Python API and inspect
the output -- file existence, content, template variable substitution. They
are fast (seconds) and need nothing beyond the test dependencies. These
tests must never modify the generated project.

**Integration tests** (`test_integration.py`) generate a project, then run
`just install`, `just test`, `just lint`, and `just gen-doc` via subprocess.
They exercise the full toolchain (uv, linkml, just) and take minutes.

### Fixture design

Generating a project with copier takes 1-3 seconds. With 80+ structural
tests, per-test generation would be very slow. To avoid this:

- **Session-scoped fixtures** (in `conftest.py`) generate each project
  variant once and share it across all structural tests. The trade-off:
  structural tests must treat the generated project as **read-only**.
- **Module-scoped fixture** for integration tests generates a fresh project
  because `just` commands mutate the project directory (installing packages,
  generating files).

Available session fixtures: `default_project`, `no_example_project`,
`no_pypi_project`, `no_docs_preview_project`, and `license_project`
(parametrized across all six license types).

### Shared helpers (`tests/helpers.py`)

| Helper | Purpose |
|--------|---------|
| `generate_project(dest, data_overrides)` | Call copier's `run_copy()` with sensible defaults |
| `git_init(project_dir)` | Init git + initial commit (needed for dynamic versioning) |
| `run_just(project_dir, *args)` | Run a just command via subprocess with timeout |
| `DEFAULT_DATA` | Dict of template variable defaults used by all tests |
| `ALL_LICENSES` | List of all six supported license identifiers |

### Adding a new structural test

1. Pick the right fixture. If you need the default project, use
   `default_project`. If you need a specific option combination that
   doesn't exist yet, add a new session-scoped fixture in `conftest.py`.
2. Put the test in the appropriate module (`test_generation.py` for general
   structure, `test_options.py` for boolean flags, `test_licenses.py` for
   license variants).
3. Never modify files inside the generated project directory -- session
   fixtures are shared.

### Adding a new integration test

Add the test to `test_integration.py`. It receives the `integration_project`
fixture which already has `just install` run in it, so dependencies are
available. Mark the test (or the whole module) with `@pytest.mark.integration`.

## CI

The GitHub Actions workflow `test-template.yml` runs two jobs:

- **structural** -- fast, Python version matrix, Ubuntu only
- **integration** -- slow, OS matrix (Ubuntu + Windows), Python version matrix

Structural tests run on every push and PR. Integration tests also run on
every push and PR but take longer, so they use a smaller matrix focused on
OS coverage.
