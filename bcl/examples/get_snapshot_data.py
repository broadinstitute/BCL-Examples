# Gets snapshot information based off a provided snapshot id
import click
from bcl.auth.obtain_session import obtain_session

staging_server = "https://gpo-staging.broadinstitute.org"


def get_snapshot_data(session, snapshot_id):
    # First get deliverable info from snapshot_id
    info_endpoint = f"https://gpo-staging.broadinstitute.org/api/deliverables?result_value={snapshot_id}"
    headers = {
        "Content-Type": "application/json",
    }
    response = session.get(url=info_endpoint, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    session = obtain_session(staging_server)

    snapshot_id = click.prompt("Enter snapshot ID")

    snapshot_data = get_snapshot_data(
        session,
        snapshot_id=snapshot_id,
    )
    print(snapshot_data)
