# script that accepts a snapshot id and a file-mapping dictionary as command-line arguments

import argparse

from common.obtain_token import obtain_session
from common.obtain_token import LoginMethod


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
    return res


def main():
    parser = argparse.ArgumentParser(description='script that accepts a snapshot id and a file-mapping dictionary as command-line arguments')
    parser.add_argument('snapshot_id', type=str, help='snapshot id')
    parser.add_argument('file_mapping', type=str, help='file mapping dictionary, e.g. {"file1": "path1", "file2": "path2"}')
    parser.add_argument('--creds', type=str,
                        help='path to service account credentials file')
    args = parser.parse_args()
    print(args.creds)

    auth_session = obtain_session(LoginMethod.FILE, args.creds)

    order = get_order(args.snapshot_id, auth_session)

    print(order)







if __name__ == '__main__':
    main()