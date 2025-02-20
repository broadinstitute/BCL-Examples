# script that accepts a snapshot id and a file-mapping dictionary as command-line arguments
import itertools
from dataclasses import dataclass
from typing import List
import argparse
import json
import urllib.request

from common.obtain_token import obtain_session
from common.obtain_token import LoginMethod

# setting these to 1 is useful for testing if you don't want to retrieve all deliverables
max_download_limit = 1
max_sample_result_limit = 1
api_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example"
    }

def parse_args():
    parser = argparse.ArgumentParser(
        description='script that accepts a snapshot id and a file-mapping dictionary as command-line arguments')
    parser.add_argument('snapshot_id', type=str, help='snapshot id')
    parser.add_argument('file_mapping', type=str,
                        help='file mapping dictionary, e.g. {"file1": "path1", "file2": "path2"}')
    parser.add_argument('--creds', type=str,
                        help='path to service account credentials file')
    parser.add_argument('--server', type=str, default='https://gpo-staging.broadinstitute.org', help='GPO server URL')
    return parser.parse_args()

# gets and parses the details for an order
def get_order(order_key, session):
    res = session.get(
        f"https://gpo-staging.broadinstitute.org/api/order/{order_key}", headers=api_headers
    )
    res.raise_for_status()

    return json.loads(res.content)

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
def extract_deliverable_urls(deliverables_url, session) -> List[DeliverableSpec]:
    response = session.get(deliverables_url, headers=api_headers)
    response.raise_for_status()
    deliverable = json.loads(response.content)
    deliverables_with_file = filter(lambda d: d.get('file'), deliverable.get('deliverables'))
    return list(map(lambda d: DeliverableSpec(d.get('name'), d.get('file').get('links').get('download')), deliverables_with_file))

@dataclass
class DownloadResult:
    url: str
    status: str

def download_deliverable(deliverable_spec: DeliverableSpec, session):
    response = session.get(deliverable_spec.url, headers=api_headers)
    response.raise_for_status()
    signed_url = response.url
    print(f"Downloading {deliverable_spec.name} from {signed_url}")
    urllib.request.urlretrieve(signed_url, "test123.txt")
    return DownloadResult(signed_url, "success")

def main():
    args = parse_args()

    auth_session = obtain_session(LoginMethod.FILE, args.creds, args.server)

    order = get_order(args.snapshot_id, auth_session)
    deliverables_urls_to_fetch = extract_deliverables_urls(order)

    deliverable_urls = []

    for deliverables_url in itertools.islice(deliverables_urls_to_fetch, max_sample_result_limit):
        deliverable_urls.extend(extract_deliverable_urls(deliverables_url, auth_session))

    download_log = []
    for deliverable_spec in itertools.islice(deliverable_urls, max_download_limit):
        download_log.append(download_deliverable(deliverable_spec, auth_session))



if __name__ == '__main__':
    main()