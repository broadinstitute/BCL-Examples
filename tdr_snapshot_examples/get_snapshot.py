# Gets snapshot information based off a provided snapshot id

import json

import click
from common.obtain_token import obtain_session

tdr_domain = "data.terra.bio"


def get_snapshot(session, payload, headers, snapshot_id):
    content_response = session.post(
        url=f"https://{tdr_domain}/api/repository/v1/snapshots/{snapshot_id}/data/sample",
        headers=headers,
        data=json.dumps(payload),
    )
    content_response.raise_for_status()
    return content_response.json()


if __name__ == "__main__":
    session = obtain_session()

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
    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot(session, domain=tdr_domain, payload=payload, headers=headers, snapshot_id=snapshot_id)
    print(snapshot_data)
