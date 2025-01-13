# LinkML Project Copier Template

> This is a new LinkML project template that uses copier instead of cruft/cookiecutter and
> replaces make by [just](https://github.com/casey/just) as command runner.
> 
> The starting point was https://github.com/linkml/linkml-project-cookiecutter/ (commit [1094cf2](https://github.com/linkml/linkml-project-cookiecutter/commit/1094cf2ce542028ab0017eaa059dd49cdde81fb5), date 2025-01-10). 
> The code from the [just command runner PR](https://github.com/linkml/linkml-project-cookiecutter/pull/127) was included (up to commit [3eb2522](https://github.com/linkml/linkml-project-cookiecutter/tree/3eb2522f5baa9e8f27ffb4ae28c0134a42d72c9d)).

A [copier](https://copier.readthedocs.io/) template for projects using [LinkML](https://github.com/linkml/linkml).

## Prerequisites

The following are required and recommended tools for using this copier template and the LinkML project that it generates. This is all one-time setup, so if you have already done it skip to the [next section](#creating-a-new-project)! We assume that you have full internet access. If not please read our section on `working in isolated environments` (tbw).

  * **git / GitHub account**

    Git is the version management system with which this template and your repository are managed. The template also assumes that you
    use GitHub for hosting your project which implies that you have a GitHub account.

  * **Python >= 3.9**
  
    LinkML tools are mainly written in Python, so you will need a recent Python interpreter to run this generator and to use the generated project.

  * **pipx**
  
    pipx is a tool for managing isolated Python-based applications. It is the recommended way to install the required tools. To install pipx follow the instructions here: https://pypa.github.io/pipx/installation/

  * **Poetry**
  
    Poetry is a Python project management tool. You will use it in your generated project to manage dependencies and build distribution files. Install Poetry by running:
     ```shell
     pipx install poetry
     ```

  * **Poetry Dynamic Versioning Plugin**: 

    This plugin automatically updates certain version strings in your generated project when you publish it. Your generated project will automatically be set up to use it. Install it by running:

    ```shell
    pipx inject poetry "poetry-dynamic-versioning[plugin]"
    ```

  * **copier**

    Copier is a tool for generating projects based on a template (like this one!). 
    It also allows re-configuring the projects and to keep them update if the original template changes.
    To insert dates into the template, copier requires [jinja2_time](https://github.com/hackebrot/jinja2-time) in the copier environment.
    Install both with pipx by running:
    ```shell
    pipx install copier
    pipx inject copier jinja2_time
    ```

  * **just**

    The project contains a `justfile` with pre-defined complex commands. 
    To execute these commands you need [just](https://github.com/casey/just) as command runner. Install it by running:
    ```shell
    pipx install just
    ```

## Creating a new project

### Step 1: Generate the project files

To generate a new LinkML project in a new subdirectory run the following:
```bash
copier create https://github.com/dalito/linkml-project-copier
```

You will be prompted a few questions.
The defaults are fine for most projects, but pick the name for your project carefully as it will also be used as project name on GitHub.

### Step 2: Set up the LinkML project

Change to the folder your generated project is in.

Optionally customize your project if needed:

* pass arguments to linkml generators via 'config.yaml' configuration file;
* pass supported environment variables via '.env.public' configuration file;

Setup your project
```bash
cd my-awesome-schema  # using the folder example above
make setup
```

### Step 3: Edit the schema

Edit the schema (the .yaml file) in the
`src/my_awesome_schema/schema` folder

```bash
nano src/my_awesome_schema/schema/my_awesome_schema.yaml
```

### Step 4: Validate the schema

```bash
just test
```

### Step 5: Generate documentation locally

LinkML generates schema documentation automatically. The template comes with GitHub Actions that generate and publish the documentation when you push schema changes to GitHub. The published documentation can be found at a URL like this one:
`https://{github-user-or-organization}.github.io/{project-name}/`

You can also preview the documentation locally before pushing to GitHub by running:

```bash
just testdoc
```

### Step 6: Create a GitHub project

1. Go to https://github.com/new and follow the instructions, being sure to NOT add a `README` or `.gitignore` file (this copier template will take care of those files for you)

2. Add the remote to your local git repository

   ```bash
   git remote add origin https://github.com/{github-user-or-organization}/{project-name}.git
   git branch -M main
   git push -u origin main
   ```

3. Configure your repository for deploying the documentation as GitHub pages

* Under Settings > Actions > General in section "Workflow Permissions" mark "Read repository and packages permission".
* Under Pages in section "Build and Deployment":
  * Under "Source" select "Deploy from a branch"
  * Under "Branch" select "gh-pages" and "/ (root)"

### Step 7: Register the schema

See [How to register a schema](https://linkml.io/linkml/faq/contributing.html#how-do-i-register-my-schema)

### Making releases

See [How to Manage Releases of your LinkML Schema](https://linkml.io/linkml/howtos/manage-releases.html)

## Keeping your project up to date

In order to be up-to-date with the template, first check if there is a mismatch
between the project's boilerplate code and the template by running:

```bash
cruft check
```

This indicates if there is a difference between the current project's
boilerplate code and the latest version of the project template. If the project
is up-to-date with the template:

```output
SUCCESS: Good work! Project's cruft is up to date and as clean as possible :).
```

Otherwise, it will indicate that the project's boilerplate code is not
up-to-date by the following:

```output
FAILURE: Project's cruft is out of date! Run `cruft update` to clean this mess up.
```

For viewing the difference, run `cruft diff`. This shows the difference between the project's boilerplate code and the template's latest version.

After running `cruft update`, the project's boilerplate code will be updated to the latest version of the template.
