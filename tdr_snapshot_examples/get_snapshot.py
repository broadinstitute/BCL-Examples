# Gets snapshot information based off a provided snapshot id

import json

import click
from common.obtain_token import obtain_session

tdr_domain = "data.terra.bio"


def get_snapshot(session, snapshot_id):
    """
    This function gets a specified snapshot from tdr.

    Args:
        session: The session in which the order will be created. If no session is given, then
                one will be obtained in the function.
        snapshot_id: The id of the snapshot to get.
    Returns:
        The json of the file from the request.
    """
    tdr_domain = "data.terra.bio"
    payload = {
        "offset": 0,
        "limit": 30,
        "sort": "datarepo_row_id",
        "direction": "asc",
        "filter": "",
    }
    headers = {
        "User-Agent": "GPO Bound Query",
        "Content-Type": "application/json",
    }
    content_response = session.post(
        url=f"https://{tdr_domain}/api/repository/v1/snapshots/{snapshot_id}/data/sample",
        headers=headers,
        data=json.dumps(payload),
    )
    content_response.raise_for_status()
    return content_response.json()


if __name__ == "__main__":
    session = obtain_session()

    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot(
        session,
        snapshot_id=snapshot_id,
    )
    print(snapshot_data)
