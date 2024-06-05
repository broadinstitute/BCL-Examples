# This file goes through the full flow of getting a snapshot,
# getting it's report's drs info, and then downloading the report
# to the file system.

import json

from get_file_info_by_drs_path import get_file_info_by_drs_path
from get_snapshot import get_snapshot
from obtain_token import obtain_session


tdr_domain = "data.terra.bio"

headers = {
    "User-Agent": "GPO Bound Query",
    "Content-Type": "application/json",
}


def download_file_from_drs(session, drs_json):
    resp = session.get(url=drs_json["accessUrl"]["url"], headers=headers)
    with open(f"{drs_json['fileName']}", "wb") as report_file:
        report_file.write(resp.content)
        report_file.close()


if __name__ == "__main__":
    session = obtain_session()
    print("==>Snapshot Information")
    snapshot_data = get_snapshot(session)
    # For each row in the result
    for snapshot_content in snapshot_data["result"]:
        print(f"==>results value is {snapshot_content['pass_fail_value']}")
        print(f"==>sample id is {snapshot_content['collaborator_sample_id']}")
        # Check which reports it has and download them
        if snapshot_content.get("technical_report"):
            print(
                f"==>Technical Report drs: {json.dumps(snapshot_content['technical_report'])}"
            )
            drs_json = get_file_info_by_drs_path(
                session, snapshot_content["technical_report"]
            )
            download_file_from_drs(session, drs_json)
        if snapshot_content.get("indication_based_report"):
            for drs in snapshot_content["indication_based_report"]:
                print(f"==>Indication Based Report drs: {json.dumps(drs)}")
                drs_json = get_file_info_by_drs_path(session, drs)
                download_file_from_drs(session, drs_json)

        if snapshot_content.get("panel_report"):
            for drs in snapshot_content["panel_report"]:
                print(f"==>Panel Report drs: {json.dumps(drs)}")
                drs_json = get_file_info_by_drs_path(session, drs)
                download_file_from_drs(session, drs_json)
