# BCL-Examples

Storehouse of Scripts to share with our API customers to assist with their interactions with BCL Orders

# Setting up your environment

> This repository uses python. You can find instructions on installing python and setting up a virtual environment [here](docs/PYTHON.md)

> There are also a few dependencies that need to be installed with pip. You can find instruction on installing those dependencies [here](docs/PIP.md)

# Token Generation

> In [`common/obtain_token.py`](common/obtain_token.py) we generate our valid token and session for all the other requests we make in this library. We have 3 ways to generate a valid authorized session.

- With the email of a user who has the proper permissions, this will commonly be a service account.
- With a saved credentials file on the current system.
- From within the google compute engine.

> By default the file uses an email, but this can be changed to fit your needs.

# Gpo Examples

> This directory contains our code for accessing GPO and performing some operations such as creating an order. You can find more information [here](gpo_examples/gpo.md)

# Terra Examples

> This directory contains our code for accessing tdr and performing operations involving snapshots. You can find more information [here](tdr_snapshot_examples/tdr.md)
