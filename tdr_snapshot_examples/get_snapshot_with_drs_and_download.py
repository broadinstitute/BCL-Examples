# This file goes through the full flow of getting a snapshot,
# getting it's report's drs info, and then downloading the report
# to the file system.

import json

import click as click

from extract_files_in_tdr_snapshot_from_snapshot_id import auth_session
from get_file_info_by_drs_path import get_file_info_by_drs_path
from get_snapshot import get_snapshot
from common.obtain_token import obtain_session
from tdr_snapshot_examples.get_file_info_by_drs_path import get_file_info_by_drs_path


def download_file_from_drs(session, drs_json):
    """
    This function downloads file information by using the link inside drs_json
    and saves it to your directory. This includes both pdf files and json files.

    Args:
        session: The session in which the order will be created. If no session is given, then
                one will be obtained in the function.
        drs_json: The json formatted file information obatined from the drs path of the file.
        headers: The headers of the get request.
    """
    headers = {
        "User-Agent": "GPO Bound Query",
        "Content-Type": "application/json",
    }

    resp = session.get(url=drs_json["accessUrl"]["url"], headers=headers)
    with open(f"{drs_json['fileName']}", "wb") as report_file:
        report_file.write(resp.content)
        report_file.close()


def retrieve_report_field_content(report_index):
    report_content = report_index
    if isinstance(report_index, str):
        report_content = [report_index]
    for report in report_content:
        drs_json = get_file_info_by_drs_path(auth_session, report)

        print(f"==>file name is {drs_json['fileName']}")
        print(f"==>gsUri is {drs_json['gsUri']}")
        print(
            f"==> Access Url for downloading is {drs_json['accessUrl']['url']}"
        )
        print(
            f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{drs_json['accessUrl']['url']}\" \n\n"
        )
        download_file_from_drs(session=auth_session, drs_json=drs_json)


if __name__ == "__main__":
    session = obtain_session()

    print("==>Snapshot Information")
    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot(session,snapshot_id=snapshot_id)
    # For each row in the result
    if snapshot_data["result"]:
        for snapshot_content in snapshot_data["result"]:
            print(f"==>results value is {snapshot_content['pass_fail_value']}")
            print(f"==>sample id is {snapshot_content['collaborator_sample_id']}")
            # Check which reports it has and download them
            if snapshot_content.get("technical_report"):
                print(
                    f"==>Technical Report drs: {json.dumps(snapshot_content['technical_report'])}"
                )
                retrieve_report_field_content(snapshot_content["technical_report"])
            if snapshot_content.get("indication_based_report"):
                print(f"==>Indication Based Report drs: {json.dumps(snapshot_content['indication_based_report'])}")
                retrieve_report_field_content(snapshot_content["indication_based_report"])

            if snapshot_content.get("panel_report"):
                print(f"==>Panel Report drs: {json.dumps(snapshot_content['indication_based_report'])}")
                retrieve_report_field_content(snapshot_content["indication_based_report"])

