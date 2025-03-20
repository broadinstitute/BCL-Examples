# This file goes through the full flow of getting a snapshot,
# getting it's report's drs info, and then downloading the report
# to the file system.

import json
from typing import TYPE_CHECKING

import click as click

from deliverables_examples.get_snapshot import get_snapshot, obtain_session

staging_server = "https://gpo-staging.broadinstitute.org"


def download_file_from_gpo(session, file):
    """
    This function downloads file information by using the GPO download deliverables endpoint
    https://gpo-staging.broadinstitute.org/api/deliverable/{result_value}/{file_id}/{filename}
    and saves it to your directory. This includes both pdf files and json files.

    Args:
        session: The session in which the order will be created. If no session is given, then
                 one will be obtained in the function.
        file: The file object given by GPO's find deliverables endpoint
              https://gpo-staging.broadinstitute.org/api/deliverables

    """
    print(f"==>file name is {file['filename']}")
    print(f"==> Access Url for downloading is {file['links']['download']}")
    print(
        f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{file['links']['download']}\" \n\n"
    )
    headers = {
        "User-Agent": "GPO Bound Query",
        "Content-Type": "application/json",
    }

    resp = session.get(url=file["links"]["download"], headers=headers)
    with open(f"{file['filename']}", "wb") as report_file:
        report_file.write(resp.content)
        report_file.close()


if __name__ == "__main__":
    session = obtain_session(staging_server)

    print("==>Snapshot Information")
    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot(session, snapshot_id=snapshot_id)
    # For each row in the result
    if snapshot_data["deliverables"]:
        for snapshot_content in snapshot_data["deliverables"]:
            if snapshot_content["name"] in [
                "pass_fail_value",
                "collaborator_sample_id",
            ]:
                print(snapshot_content["order_id"])
                print(snapshot_content["sidr_sample_id"])
                print(
                    f"{snapshot_content['name']} has a value of {snapshot_content['value']}\n"
                )
            elif snapshot_content["name"] in [
                "technical_report",
                "indication_based_report",
                "panel_report",
            ]:
                download_file_from_gpo(session, snapshot_content["file"])
