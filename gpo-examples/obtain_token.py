# This file generates a valid google session using credentials and a token

import warnings
import click
from google.oauth2 import service_account
import google.auth
import google.auth.transport.requests
from google.auth.transport.requests import AuthorizedSession
from google.auth import compute_engine
from google.auth import impersonated_credentials, jwt
from google.auth.transport import requests  # type: ignore

# Sets the tokens audience
target_audience = click.prompt(
    "Specify the target Audience", default="https://gpo-staging.broadinstitute.org"
)


# If you want to use a human account or service account
def get_creds_from_human_user():
    service_account_email = click.prompt("Specify account email to be used")
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            "Your application has authenticated using end user credentials from"
            " Google Cloud SDK.",
        )
        user_creds, _ = google.auth.default()

    user_creds.refresh(requests.Request())

    # Ensure the user is authenticated with gcloud
    target_creds = impersonated_credentials.Credentials(
        source_credentials=user_creds,
        target_principal=service_account_email,
        target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    target_creds.refresh(requests.Request())

    return impersonated_credentials.IDTokenCredentials(
        target_credentials=target_creds,
        target_audience=target_audience,
        include_email=True,
    )


# If your running outside of compute engine and not associated with a human user
def get_creds_from_file():
    return service_account.IDTokenCredentials.from_service_account_file(
        "path/to/svc.json", target_audience=target_audience
    )


# If running in google cloud compute engine
def get_creds_from_within_compute_engine():
    request = google.auth.transport.requests.Request()
    return compute_engine.IDTokenCredentials(request, target_audience=target_audience)


def obtain_session():
    # Change this method to whichever credential method you want
    creds = get_creds_from_human_user()
    # Create the session
    authed_session = AuthorizedSession(creds)
    # Need this initial request to generate the token for tdr usage
    authed_session.get(
        "https://gpo-staging.broadinstitute.org/auth",
        headers={"User-Agent": "bcl-example"},
    )
    return authed_session


if __name__ == "__main__":

    authed_session = obtain_session()
    # Use authorized session to make a request to gpo
    resp = authed_session.get(
        "https://gpo-staging.broadinstitute.org/auth",
        headers={"User-Agent": "bcl-example"},
    )
    print(resp.status_code)
    print(resp.text)
