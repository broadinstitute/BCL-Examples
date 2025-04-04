# BCL-Examples

Examples scripts for organizations looking to place orders, monitor order status, and retrieve results from BCL Orders.

# Environment Setup

This repository uses Python and was developed using Python 3.11. These scripts should work with any recent version of Python 3. Dependencies for this repo are outlined in [requirements.txt](requirements.txt)

* Instructions for installing Python and setting up a Virtual Environment can be found [here](docs/PYTHON.md)
* Dependencies can be installed using `pip install -r requirements.txt -r requirements-google.txt`

# Directory

* [bcl/examples](bcl/examples): Example scripts showing how a customer integration might work with GPO
* [bcl/helpers](bcl/helpers): Helper scripts for setting up new integrations with GPO
* [bcl/auth](bcl/auth): Components for implementing authentication described below

# Running Examples

These examples rely on this repo being in PYTHONPATH. This can be accomplished by running the examples directly:

```
./bcl/examples/get_orders.py -d
```

or manually:

```
env PYTHONPATH=$PWD python ./bcl/examples/get_orders.py -d
```


# Authentication

BCL Orders supports several methods of authenticating.
Currently, these examples are created using Google Cloud Platform (GCP) IAM as an Authentication Provider to authenticate a GCP Service Account.
Please contact support if you would like to use a different authentication system.

## GCP Service Account Authentication

There are 3 options that can be used to configure these scripts to authenticate with GPO using Google Cloud Platform Service Accounts.
These scripts use the standards outlined in https://google.aip.dev/auth/4110 to accept credentials

### GCP Service Account Keys
For fixed installations, it might be desirable to create a service account key file that will allow scripts to authenticate with GPO indefinitely.
Follow these steps to authenticate using Service Account Keys:

1) Create and store a JSON key for a GCP Service Account following the instructions here: https://cloud.google.com/iam/docs/keys-create-delete
2) Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the location on the file system of this key. IE: `GOOGLE_APPLICATION_CREDENTIALS=/home/my-user/my-service-account-key.json`
3) Research security concerns associated with Service Account Keys and ensure key is stored securely and rotated based on your organizations information security needs. See https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys for first steps.

### GCP Service Account Impersonation
For running scripts locally, it is possible to impersonate a service account using the `gcloud` tool's Application Default Credentials.
This method relies on the current human user having permission to impersonate the service account.
Follow these steps to authenticate using GCP Service Account Impersonation:

1) Install and configure `gcloud`: https://cloud.google.com/sdk/docs/install
2) Generate Application Default Credentials using Impersonation: `gcloud auth application-default login --impersonate-service-account my-service-account@my-project.iam.gserviceaccount.com` (See https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment#sa-impersonation)
3) Set GOOGLE_APPLICATION_CREDENTIALS to the path to your gcloud application default credentials: `GOOGLE_APPLICATION_CREDENTIALS=$HOME/.config/gcloud/application_default_credentials.json` (See https://cloud.google.com/docs/authentication/application-default-credentials#personal)

### GCP Compute Engine Metadata Server

For applications running in Google Compute Engine under a GCP Service Account, no environment variable is necessary.
The Google client library used in these scripts will automatically use the Compute Engine Metadata Server to make authenticated requests to BCL Orders' API
