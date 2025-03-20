# This file is a full end to end workflow of gettings order information
# from gpo, and then snapshot information from terra if there is any
# and saving it to your computer.

import json
from typing import TYPE_CHECKING

import click

from deliverables_examples.get_snapshot import get_snapshot
from deliverables_examples.get_snapshot_and_download_it import download_file_from_gpo
from download_deliverables import obtain_session
from gpo_examples.get_order import retrieve_gpo_orders, retrieve_gpo_order

staging_server = "https://gpo-staging.broadinstitute.org"


payload = {
    "offset": 0,
    "limit": 30,
    "sort": "datarepo_row_id",
    "direction": "asc",
    "filter": "",
}
auth_session = obtain_session(staging_server)

project_key = click.prompt(
    "Enter the BCL Project for which you wish to retrieve information.", default=""
)
order_key = click.prompt(
    "Enter the BCL Order for which you wish to retrieve information.", default=""
)

# sam_response = auth_session.get(url="https://sam.dsde-prod.broadinstitute.org/api/users/v2/self", headers=headers, data={})
# click.echo(json.dumps(sam_response.json()))
gpo_response = None
if project_key:
    gpo_response = retrieve_gpo_orders(
        email="scottmat@broadinstitute.org",
        project_key=project_key,
        session=auth_session,
    )
elif order_key:
    gpo_response = retrieve_gpo_order(
        email="ngigliot@broadinstitute.org", order_key=order_key, session=auth_session
    )

if gpo_response:
    # print(json.dumps(gpo_response.json()))
    gpo_order_json = gpo_response.json()
    if order_key:
        gpo_order_json = [gpo_order_json]
    for order in gpo_order_json:
        if order.get("order_id"):
            print(f"\n\n==> For order {order['order_id']}")
        for test in order["tests"]:
            for sample in test["test_samples"]:
                if sample.get("sample_id"):
                    print(f"==> Sample ID is {sample['sample_id']}")
                if sample.get("client_barcode"):
                    print(f"==> Vessel Barcode is {sample['client_barcode']}")
                print(f"==> SIDR Sample ID is {sample['sidr_sample_id']}")
                print(f"==> Sample status is {sample['test_sample_status']}")
                for result in sample.get("results"):
                    snapshot_id = result["result_value"]

                    print("------Getting content of snapshot------")
                    content_response = get_snapshot(
                        session=auth_session,
                        snapshot_id=snapshot_id,
                    )

                    print(json.dumps(content_response))
                    if content_response["deliverables"]:
                        for snapshot_content in content_response["deliverables"]:
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
                                download_file_from_gpo(
                                    auth_session, snapshot_content["file"]
                                )
