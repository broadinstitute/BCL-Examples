#! /bin/env python

# Get order information using Order ID returned by Create Order endpoint
import argparse
from pprint import pprint

from bcl.auth.obtain_session import obtain_session
from bcl.constants import PROD_SERVER, STAGING_SERVER


def parse_args():
    parser = argparse.ArgumentParser(
        description="script that gets an order by order key"
    )
    parser.add_argument(
        "id_to_fetch",
        type=str,
        help="order id ('SDOR-STAGING-3GJJ')",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="production server -- if set, will connect to the production server (default is staging)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Get args
    args = parse_args()

    server = PROD_SERVER if args.p else STAGING_SERVER
    session = obtain_session(server)

    res = session.get(f"{server}/api/order/{args.id_to_fetch}")
    res.raise_for_status()
    pprint(res.json())
