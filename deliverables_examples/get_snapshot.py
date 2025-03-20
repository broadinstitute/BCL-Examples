# Gets snapshot information based off a provided snapshot id

import json

import click
import google.auth
import google.auth.transport.requests
import google.auth.impersonated_credentials
import google.oauth2.id_token

staging_server = "https://gpo-staging.broadinstitute.org"


def obtain_session(target_audience):
    api_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }

    # Create and configure AuthorizedSession using ambient credentials (See https://google.aip.dev/auth/4110)
    credentials, _ = google.auth.default()
    if isinstance(credentials, google.auth.impersonated_credentials.Credentials):
        credentials = google.auth.impersonated_credentials.IDTokenCredentials(
            credentials, target_audience=target_audience
        )
    else:
        credentials = google.oauth2.id_token.fetch_id_token_credentials(
            target_audience, google.auth.transport.requests.Request()
        )
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    session.headers = api_headers
    return session


def get_snapshot(session, snapshot_id):
    # First get deliverable info from snapshot_id
    info_endpoint = f"https://gpo-staging.broadinstitute.org/api/deliverables?result_value={snapshot_id}"
    headers = {
        "Content-Type": "application/json",
    }
    response = session.get(url=info_endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    session = obtain_session(staging_server)

    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot(
        session,
        snapshot_id=snapshot_id,
    )
    print(snapshot_data)
