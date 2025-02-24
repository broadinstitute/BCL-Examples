# script that accepts a snapshot id and a file-mapping dictionary as command-line arguments
import itertools
import argparse
import json
import urllib.request
import logging
import os

import google.auth
import google.auth.transport.requests
import google.auth.impersonated_credentials
import google.oauth2.id_token

from dataclasses import dataclass
from typing import List

# Script for retrieving deliverable files from a GPO order or Snapshot.
# This uses Google Application Default Credentials to handle authentication (See https://google.aip.dev/auth/4110)
# For example, if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set, the script will look for a credentials file there.

# setting these to 1 is useful for testing if you don't want to retrieve all deliverables while testing
max_download_limit = 1
max_sample_result_limit = 1


def parse_args():
    parser = argparse.ArgumentParser(
        description="script that accepts a snapshot id and a file-mapping dictionary as command-line arguments"
    )
    parser.add_argument("order_id", type=str, help="order id")
    parser.add_argument(
        "--file_mapping",
        type=str,
        help='file mapping dictionary, e.g. {"file1": "path1", "file2": "path2"}',
        default="{}",
    )
    parser.add_argument(
        "-d",
        action="store_true",
        help="dry run -- will query endpoints to determine files to download, but will not perform the downloads",
    )
    parser.add_argument(
        "--server",
        type=str,
        default="https://gpo-staging.broadinstitute.org",
        help="GPO server URL",
    )
    return parser.parse_args()


def obtain_session(target_audience):
    api_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }

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
    session.headers = api_headers
    return session


# gets and parses the details for an order
def get_order(order_key, session, server: str):
    res = session.get(f"{server}/api/order/{order_key}")
    res.raise_for_status()
    return res.json()


# returns a list of urls to fetch deliverables from
def extract_deliverables_urls(order):
    urls_to_fetch: List[str] = []
    # for each test, iterate through the samples, and for each sample, iterate through the results
    for test in order["tests"]:
        for sample in test["test_samples"]:
            for result in sample["results"]:
                deliverables_url = result.get("links", {}).get("deliverables")
                urls_to_fetch.append(deliverables_url)
    return urls_to_fetch


@dataclass
class DeliverableSpec:
    name: str
    url: str


# returns a list of dictionaries, each with the name and url of the deliverable
def extract_deliverable_specs(deliverables_url, session) -> List[DeliverableSpec]:
    response = session.get(deliverables_url)
    response.raise_for_status()
    deliverable = json.loads(response.content)
    deliverables_with_file = filter(
        lambda d: d.get("file"), deliverable.get("deliverables")
    )
    return list(
        map(
            lambda d: DeliverableSpec(
                d.get("name"), d.get("file").get("links").get("download")
            ),
            deliverables_with_file,
        )
    )


@dataclass
class DownloadResult:
    url: str
    status: str


def download_deliverable(
    deliverable_spec: DeliverableSpec, file_name, session, is_dry_run: bool = False
):
    if is_dry_run:
        logging.info(
            f"Would download {deliverable_spec.name} from {deliverable_spec.url}"
        )
        return DownloadResult(deliverable_spec.url, "skipped")

    logging.info(f"Downloading {deliverable_spec.name} from {deliverable_spec.url}")
    response = session.get(deliverable_spec.url)
    response.raise_for_status()
    signed_url = response.url

    urllib.request.urlretrieve(signed_url, file_name)
    logging.info(
        f"Downloaded {deliverable_spec.name} from {deliverable_spec.url} - success"
    )
    return DownloadResult(deliverable_spec.url, "success")


def main():
    # Configure logging:
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    args = parse_args()
    file_mapping = json.loads(args.file_mapping or "{}")
    auth_session = obtain_session(args.server)

    order = get_order(args.order_id, auth_session, args.server)
    deliverables_urls_to_fetch = extract_deliverables_urls(order)

    logging.info(
        f"Found {len(deliverables_urls_to_fetch)} result(s) with deliverables to download"
    )
    if (
        max_sample_result_limit
        and len(deliverables_urls_to_fetch) > max_sample_result_limit
    ):
        logging.info(f"Limiting to {max_sample_result_limit} result(s)")
        deliverables_urls_to_fetch = itertools.islice(
            deliverables_urls_to_fetch, max_sample_result_limit
        )
    deliverable_specs = []
    for deliverables_url in deliverables_urls_to_fetch:
        deliverable_specs.extend(
            extract_deliverable_specs(deliverables_url, auth_session)
        )

    print(f"Found {len(deliverable_specs)} file(s) to download")
    if max_download_limit and len(deliverable_specs) > max_download_limit:
        print(f"Limiting to first {max_sample_result_limit} file(s)")
        deliverable_specs = itertools.islice(deliverable_specs, max_download_limit)
    download_log = []
    for deliverable_spec in deliverable_specs:
        download_log.append(
            download_deliverable(
                deliverable_spec,
                file_mapping.get(deliverable_spec.name, deliverable_spec.name),
                auth_session,
                args.d,
            )
        )


if __name__ == "__main__":
    main()
