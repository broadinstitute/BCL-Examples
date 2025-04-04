# script that accepts a snapshot id and a file-mapping dictionary as command-line arguments
import argparse
import datetime
import hashlib
import json
import logging
import os
import urllib.request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List
from uuid import UUID

from bcl.auth.obtain_session import obtain_session
from bcl.constants import PROD_SERVER, STAGING_SERVER


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
        help='file mapping dictionary, e.g. {"cram_path": "cram", "crai_path": "crai"}',
        default="{}",
    )
    parser.add_argument(
        "--target_dir",
        type=str,
        help="target folder for placing the downloaded files.  Default is `./deliverables/{id_to_fetch}",
        default="./deliverables/{id_to_fetch}",
    )
    parser.add_argument(
        "-d",
        action="store_true",
        help="dry run -- will query endpoints to determine files to download, but will not perform the downloads",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        help="production server -- if set, will connect to the production server (default is staging)",
    )
    parser.add_argument(
        "-c",
        action="store_true",
        help="allow clobber.  By default, this script wil not overwrite files that already exist in the target directory",
    )
    parser.add_argument(
        "--max_download_limit",
        default=None,
        help="useful for testing if you don't want to retrieve all deliverables while testing",
    )
    return parser.parse_args()


@dataclass
class DeliverableSpec:
    name: str
    url: str
    md5_url: str | None = None


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


def pair_deliverable_with_md5(
    deliverable_specs: List[DeliverableSpec],
) -> List[DeliverableSpec]:
    # This function pairs deliverables with their corresponding md5 files
    # The md5 file is expected to be in the same directory as the deliverable
    # and have the same name with "_md5_" inserted before the path
    deliverable_specs.sort(key=lambda x: x.name)
    md5_specs = [d for d in deliverable_specs if "_md5_" in d.name]
    file_specs = [d for d in deliverable_specs if "_md5_" not in d.name]
    paired_specs = []
    for deliverable_spec in file_specs:
        # to
        md5_name = f"{deliverable_spec.name[:-5]}_md5_path"
        md5_spec = next(
            (md5 for md5 in md5_specs if md5.name == md5_name),
            None,
        )
        paired_specs.append(
            DeliverableSpec(
                deliverable_spec.name,
                deliverable_spec.url,
                md5_spec.url if md5_spec else None,
            )
        )
    return paired_specs


def md5(fname):
    hash_md5 = hashlib.md5()
    hash_md5.update(open(fname, "rb").read())
    return hash_md5.hexdigest()


@dataclass
class DownloadResult:
    name: str
    url: str
    status: str
    path: str
    md5: str | None = None
    date: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error: str | None = None  # time the download finished or errored


def fetch_with_redirect(url, file_name, session):
    logging.info(f"Downloading {file_name} from {url}")
    response = session.get(url)
    response.raise_for_status()
    signed_url = response.url
    # make the containing directory if it doesn't exist -- in case it was specified in the map
    Path(os.path.dirname(file_name)).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(signed_url, file_name)
    logging.info(f"Downloaded {file_name} from {url} - success")


def download_deliverable(
    deliverable_spec: DeliverableSpec,
    file_name,
    session,
    is_dry_run: bool = False,
    allow_clobber: bool = False,
):
    if is_dry_run:
        logging.info(f"Would download {file_name} from {deliverable_spec.url}")
        return DownloadResult(
            deliverable_spec.name, deliverable_spec.url, "skipped", file_name
        )
    if os.path.exists(file_name) and not allow_clobber:
        logging.info(f"Skipping download - {file_name} already exists")
        return DownloadResult(
            deliverable_spec.name, deliverable_spec.url, "skipped", file_name
        )
    try:

        fetch_with_redirect(deliverable_spec.url, file_name, session)
        file_md5 = ""
        if deliverable_spec.md5_url:
            fetch_with_redirect(deliverable_spec.md5_url, file_name + ".md5", session)
            file_md5 = md5(file_name)
            expected_md5 = open(file_name + ".md5", "r").read().strip()
            if file_md5 == expected_md5:
                logging.info(f"MD5 check passed for {file_name} - {file_md5}")
            else:
                raise Exception(
                    f"MD5 check failed for {file_name} - file md5 was {file_md5}, expected {expected_md5}"
                )

        return DownloadResult(
            deliverable_spec.name,
            deliverable_spec.url,
            "downloaded",
            file_name,
            file_md5,
        )
    except Exception as e:
        logging.error(f"Failed to download {file_name} from {deliverable_spec.url}")
        logging.error(e)
        return DownloadResult(
            deliverable_spec.name,
            deliverable_spec.url,
            "failed",
            file_name,
            error=str(e),
        )


class IdType(Enum):
    ORDER = "order_id"
    SNAPSHOT = "result_value"


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

    target_dir = args.target_dir or "./"
    target_dir = target_dir.format(id_to_fetch=args.id_to_fetch)
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    file_mapping = json.loads(args.file_mapping or "{}")

    server = PROD_SERVER if args.p else STAGING_SERVER
    session = obtain_session(server)

    id_to_fetch = args.id_to_fetch
    id_type = determine_id_type(id_to_fetch)
    deliverables_urls_to_fetch = [
        f"{server}/api/deliverables?{id_type.value}={id_to_fetch}"
    ]

    deliverable_specs = []
    for deliverables_url in deliverables_urls_to_fetch:
        deliverable_specs.extend(extract_deliverable_specs(deliverables_url, session))

    print(f"Found {len(deliverable_specs)} file(s) to download")
    if args.max_download_limit and len(deliverable_specs) > args.max_download_limit:
        print(f"Limiting to first {args.max_download_limit} file(s)")
        deliverable_specs = deliverable_specs[: args.max_download_limit]

    paired_specs = pair_deliverable_with_md5(deliverable_specs)

    manifest_file_name = os.path.join(target_dir, "manifest.txt")
    with open(manifest_file_name, "a") as f:
        f.write("time, type, status, path, url, md5, error\n")

    for deliverable_spec in paired_specs:
        download_dest = os.path.join(
            target_dir, file_mapping.get(deliverable_spec.name, deliverable_spec.name)
        )
        result = download_deliverable(
            deliverable_spec,
            download_dest,
            session,
            is_dry_run=args.d,
            allow_clobber=args.c,
        )
        with open(manifest_file_name, "a") as f:
            f.write(
                f"{result.date}, {result.name}, {result.status}, {result.path}, {result.url}, {result.md5}, {result.error}\n"
            )

    logging.info("Download process complete")


if __name__ == "__main__":
    main()
