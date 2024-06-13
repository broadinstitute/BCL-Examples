# Python Package Management

> This project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage dependencies.

## Requirement Files

Requirements files separate the dependencies you need to install from the ones you don't:

- `requirements.in` contains all of the primary production dependencies. To install a new
  package needed by a running container, add it here.
- `requirements.txt` contains a compiled lock file of the actual dependencies used in
  production and development containers, including all nested sub-dependencies.
  Each dependency includes comments indicating why it is needed.
  [dependabot](https://github.com/dependabot) monitors these locked versions once a week to determine which to upgrade.
- `requirements-dev.in` contains all dependencies needed for running linting, code formatting
  or unit tests. These are generally not used in production containers.
- `requirements-dev.txt` contains a compiled lock file of the dependencies needed for testing.
  It does not include the dependencies listed in `requirements.txt`, but is internally consist
  with the package versions used in that file.

## Installing Dependencies

A script is used to assist to help you install all required packages, run:

```bash
./pip-install.sh
```

This script:

- Ensures `pip-tools` is installed.
- Updates `requirements.txt` and `requirements-dev.txt` if necessary to match the `.in` files.
- Installs all dependencies and uninstalls any existing ones which are not required.

> NOTE: You should only do this inside a Python virtual environment
> or it could uninstall dependencies which might be needed by other projects.

## Adding Dependencies

Add the dependency to either `requirements.in` or `requirements-dev.in`, depending
on whether the dependency is needed by production containers or only for development
and testing.

Run the script again to update the `requirements.txt` and `requirements-dev.txt` files:

```bash
./pip-install.sh
```

> NOTE: You should only need to add it to one of the files, since both files are used together in development.

## [Upgrading Dependencies](https://github.com/jazzband/pip-tools#updating-requirements)

If `pip-compile` finds an existing `requirements.txt` file that fulfills the
dependencies, then no changes will be made even if updates are available.

To force it up to upgrade all packages to the latest compatible versions:

```bash
./pip-install.sh --upgrade
```

> NOTE: You can pass any flag supported by [pip-tools](https://github.com/jazzband/pip-tools)
> to the `.pip-install.sh` command. You can also run the `pip-compile` and `pip-sync` commands
> yourself directly if you'd like.

### Upgrading Specific Dependencies

Sometimes you need to upgrade a specific dependency.
Use the `--upgrade-package` or `-P` flag. For example:

```bash
pip-compile --upgrade-package Flask --upgrade-package requests=2.0.0
```
