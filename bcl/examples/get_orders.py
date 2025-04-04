#! /bin/env python

import argparse
import datetime
import logging
import os
from pprint import pprint

from bcl.auth.obtain_session import obtain_session
from bcl.constants import PROD_SERVER, STAGING_SERVER


def parse_args():
    parser = argparse.ArgumentParser(
        description="script that gets orders using various search criteria"
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="production server -- if set, will connect to the production server (default is staging)",
    )
    parser.add_argument(
        "-d",
        action="store_true",
        help="last day -- return orders updated in the last 24 hours",
    )
    parser.add_argument(
        "-s",
        type=str,
        default=None,
        help="Sample ID -- return orders matching the given Sample ID returned when the order was created",
    )
    parser.add_argument(
        "-r",
        type=str,
        default=None,
        help="Project Key -- return orders matching the given Project Key",
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Configure logging:
    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    args = parse_args()

    server = PROD_SERVER if args.p else STAGING_SERVER
    session = obtain_session(server)

    search_criteria = {"page": ">"}  # ">" represents first page of results
    if args.d:
        start_date = (
            (datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=25))
            .replace(tzinfo=None)
            .isoformat()
        )
        search_criteria["start_date"] = start_date
    if args.s:
        search_criteria["sidr_sample_id"] = args.s
    if args.r:
        search_criteria["project_key"] = args.r

    orders = []
    while True:
        logging.info(f"Getting orders using criteria {search_criteria}")
        res = session.get(f"{server}/api/orders", params=search_criteria)
        res.raise_for_status()
        response_body = res.json()
        orders.extend(response_body["items"])
        next_page = response_body["paging"].get("next", None)
        if next_page:
            search_criteria["page"] = next_page
        else:
            break

    pprint(orders)
