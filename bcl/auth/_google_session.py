import logging

import google.auth
import google.auth.impersonated_credentials
import google.auth.transport.requests
import google.oauth2.id_token


def google_session(target_audience: str):
    # This uses Google Application Default Credentials to handle authentication (See https://google.aip.dev/auth/4110)
    # For example, if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set, the script will look for a credentials file there.

    # Create and configure AuthorizedSession using ambient credentials (See https://google.aip.dev/auth/4110)
    credentials, _ = google.auth.default()
    if isinstance(credentials, google.auth.impersonated_credentials.Credentials):
        logging.debug("Using Application Default Credentials")
        credentials = google.auth.impersonated_credentials.IDTokenCredentials(
            credentials, target_audience=target_audience
        )
    else:
        credentials = google.oauth2.id_token.fetch_id_token_credentials(
            target_audience, google.auth.transport.requests.Request()
        )
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "bcl-example",
        }
    )
    return session
