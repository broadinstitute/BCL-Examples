# script that accepts a snapshot id and a file-mapping dictionary as command-line arguments
from typing import List
import argparse
import json

from common.obtain_token import obtain_session
from common.obtain_token import LoginMethod

def parse_args():
    parser = argparse.ArgumentParser(
        description='script that accepts a snapshot id and a file-mapping dictionary as command-line arguments')
    parser.add_argument('snapshot_id', type=str, help='snapshot id')
    parser.add_argument('file_mapping', type=str,
                        help='file mapping dictionary, e.g. {"file1": "path1", "file2": "path2"}')
    parser.add_argument('--creds', type=str,
                        help='path to service account credentials file')
    return parser.parse_args()


def get_order(order_key, session):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example"
    }
    res = session.get(
        f"https://gpo-staging.broadinstitute.org/api/order/{order_key}", headers=headers
    )
    res.raise_for_status()

    return json.loads(res.content)

def extract_deliverables_urls(order):
    urls_to_fetch: List[str] = []
    # for each test, iterate through the samples, and for each sample, iterate through the results
    for test in order["tests"]:
        for sample in test["test_samples"]:
            for result in sample["results"]:
                deliverables_url = result.get("links", {}).get("deliverables")
                urls_to_fetch.append(deliverables_url)
    return urls_to_fetch

def main():
    args = parse_args()

    auth_session = obtain_session(LoginMethod.FILE, args.creds)

    order = get_order(args.snapshot_id, auth_session)
    urls_to_fetch = extract_deliverables_urls(order)

    print(urls_to_fetch)

    #for url in urls_to_fetch:
    deliverables = auth_session.get(urls_to_fetch[0])
    print(deliverables.json())

if __name__ == '__main__':
    main()