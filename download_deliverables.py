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
from uuid import UUID
from enum import Enum

# Script for retrieving deliverable files from a GPO order or Snapshot.
# This uses Google Application Default Credentials to handle authentication (See https://google.aip.dev/auth/4110)
# For example, if the GOOGLE_APPLICATION_CREDENTIALS environment variable is set, the script will look for a credentials file there.


def parse_args():
    parser = argparse.ArgumentParser(
        description="script that accepts a snapshot id and a file-mapping dictionary as command-line arguments"
    )
    parser.add_argument(
        "id_to_fetch",
        type=str,
        help="order id ('SDOR-STAGING-3GJJ') or snapshot id (''e0d21523-2b01-457e-bd85-4cba4b687727')  ",
    )
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
        "--max_download_limit",
        help="useful for testing if you don't want to retrieve all deliverables while testing",
    )
    parser.add_argument(
        "--max_sample_result_limit",
        help="useful for testing if you don't want to retrieve all results for a given sample",
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


class IdType(Enum):
    ORDER = "order"
    SNAPSHOT = "snapshot"


def determine_id_type(id_to_fetch: str) -> IdType:
    try:
        UUID(id_to_fetch)
        return IdType.SNAPSHOT
    except ValueError:
        return IdType.ORDER


def main():
    # Configure logging:
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    args = parse_args()
    file_mapping = json.loads(args.file_mapping or "{}")
    sesstion = obtain_session(args.server)

    id_to_fetch = args.id_to_fetch
    id_type = determine_id_type(id_to_fetch)

    if id_type == IdType.ORDER:
        deliverables_urls_to_fetch = [
            f"{args.server}/api/deliverables?order_id={id_to_fetch}"
        ]
    else:
        deliverables_urls_to_fetch = [
            f"{args.server}/api/deliverables?result_value={id_to_fetch}"
        ]

    deliverable_specs = []
    for deliverables_url in deliverables_urls_to_fetch:
        deliverable_specs.extend(extract_deliverable_specs(deliverables_url, sesstion))

    print(f"Found {len(deliverable_specs)} file(s) to download")
    if args.max_download_limit and len(deliverable_specs) > args.max_download_limit:
        print(f"Limiting to first {args.max_download_limit} file(s)")
        deliverable_specs = deliverable_specs[: args.max_download_limit]
    download_log = []
    for deliverable_spec in deliverable_specs:
        download_log.append(
            download_deliverable(
                deliverable_spec,
                file_mapping.get(deliverable_spec.name, deliverable_spec.name),
                sesstion,
                args.d,
            )
        )


if __name__ == "__main__":
    main()
