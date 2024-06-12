# BCL-Examples

Storehouse of Scripts to share with our API customers to assist with their interactions with BCL Orders

# Setting up your environment

> This repository uses python. You can find instructions on installing python and setting up a virtual environment [here](docs/PYTHON.md)

> There are also a few dependencies that need to be installed with pip. You can find instruction on installing those dependencies [here](docs/PIP.md)

# Token Generation

> In [`common/obtain_token.py`](common/obtain_token.py) we generate our valid token and session for all the other requests we make in this library. We have 3 ways to generate a valid authorized session.

- Service Account Impersonation: Uses the email of a service account to generate the credentials.
- Credentials File: Uses a saved credentials file on the current system to generate the credentials.
- Google Compute: Uses the Google Compute Engine to generate the credentials.

> By default the file uses Service Account Impersonation, but this can be changed to fit your needs.

# Gpo Library

> This library contains code for accessing GPO and performing some operations such as creating an order. You can find more information [here](gpo_examples/gpo.md)

# Terra Library

> This library contains our code for accessing tdr and performing operations involving snapshots. You can find more information [here](tdr_snapshot_examples/tdr.md)

# End to End Example

The file `extract_files_in_tdr_snapshot_from_snapshot_id.py` is an example of using the libraries end to end from retrieving data from GPO to extracting from TDR.
