# Python Installation

> If you plan to do local development in an IDE, you need to install Python and link your IDE.
> This will let you run tests locally and do proper type validation and autocompletion.
>
> If you only need to do deployments or run tests in Docker, you can skip this whole section.

## Installing Python 3.11.x

There several ways to install Python.

### Option 1: Direct Download

[Download and install it directly](https://www.python.org/downloads/).
Depending on your OS, this may conflict with the default version packaged with your OS.

### Option 2: `pyenv`

Use [pyenv](https://github.com/pyenv/pyenv) to manage multiple Python versions.

> NOTE: For Linux, view the [Linux Docs](LINUX.md).

Install [pyenv](https://github.com/pyenv/pyenv#installation):

```bash
brew install pyenv
```

[Mount pyenv into your system `$PATH`](https://github.com/pyenv/pyenv#basic-github-checkout):

- On Mac, you'll likely need to add it to your `zshrc` instead:
  ```bash
  echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
  ```

Download the latest version of Python 3.11.x:

```bash
pyenv install 3.11
```

It may prompt you to select a sub-version. If so, select the latest one (`3.11.4` at the time of this writing).

> NOTE: Make sure you restart your shell after this!!

Activate Python 3.11:

- To use it in your local shell until you create a Virtual Environment:

```bash
pyenv shell 3.11.4
```

- To activate it globally:

```bash
pyenv global 3.11.4
```

Verify your Python version:

```bash
# see where the Python executable is:
which python

# see what version Python thinks it is:
python --version
```

## Virtual Environment

To avoid conflicts with packages, it is best practice to use a Virtual Environment.
This will create a "sandbox" for your project.

> For the below instructions, the Virtual Environment is in the `.venv` directory.
> You can also install it in `venv` without the leading period.

### Manual Creation

Create a virtual environment and activate it:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

This should create a new virtual environment based on the active version of Python,
which should be 3.11 since you activated it above.

> NOTE: It's possible that `.venv` won't respect your preferred python version and will choose the system default
> version instead. In that case, install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
> to manage your virtual environment in the context of the python environment.

## To Upgrade your version of Python:  (3.10 -> 3.11, etc)

>
> You can support two version of Python at once by using both directories!

To test a new version of Python before switching to it permanently, create a new
virtual environment in the other `venv` directory.
(For example, if you have Python 3.10 installed in `.venv`, consider installing Python 3.11 in `venv`).
Or, you can just delete your current virtual environment directory and recreate it.

Follow the instructions from above, like this:

```shell
# Download the latest version of python
pyenv install 3.11

# Activate the latest version in your shell
pyenv local 3.11.4  # or whatever version was downloaded

# Optionally, delete the old virtual environment
rm -rf .venv

# Create a new virtual environment in your project (either in the .venv or venv directory)
python -m venv .venv

# Activate the new virtual environment in your shell
source .venv/bin/activate

# Upgrade pip and pip-tools
pip install --upgrade pip

# Install all dependencies
pip install requirements.txt requirements-google.txt
```

