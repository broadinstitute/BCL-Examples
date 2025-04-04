#! /bin/env python

# Get Metadata for project and test
import argparse
from pprint import pprint

from bcl.auth.obtain_session import obtain_session
from bcl.constants import PROD_SERVER, STAGING_SERVER


def parse_args():
    parser = argparse.ArgumentParser(
        description="script that gets test metadata by project and returns the response."
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="production server -- if set, will connect to the production server (default is staging)",
    )
    parser.add_argument(
        "project_key",
        type=str,
        help="project to retrieve metadata for",
    )
    parser.add_argument(
        "test_code",
        type=str,
        help="test code to retrieve metadata for",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Get args
    args = parse_args()

    server = PROD_SERVER if args.p else STAGING_SERVER
    session = obtain_session(server)

    res = session.get(
        f"{server}/api/catalog/metadata/project/{args.project_key}/test/{args.test_code}",
    )
    res.raise_for_status()

    pprint(res.json())
