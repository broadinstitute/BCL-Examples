# This file is a full end to end workflow of gettings order information
# from gpo, and then snapshot information from terra if there is any
# and saving it to your computer.

import json
from typing import TYPE_CHECKING

import click

from gpo_examples.get_order import retrieve_gpo_orders, retrieve_gpo_order

from tdr_snapshot_examples.get_snapshot import get_snapshot
from common.obtain_token import obtain_session
from tdr_snapshot_examples.get_snapshot_with_drs_and_download import retrieve_report_field_content

tdr_domain = "data.terra.bio"

payload = {
    "offset": 0,
    "limit": 30,
    "sort": "datarepo_row_id",
    "direction": "asc",
    "filter": "",
}
auth_session = obtain_session()

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
        email="scottmat@broadinstitute.org", order_key=order_key, session=auth_session
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
                if sample.get('sample_id'):
                    print(f"==> Sample ID is {sample['sample_id']}")
                if sample.get('client_barcode'):
                    print(f"==> Vessel Barcode is {sample['client_barcode']}")
                print(f"==> SIDR Sample ID is {sample['sidr_sample_id']}")
                print(f"==> Sample status is {sample['test_sample_status']}")
                if sample.get("results"):
                    for result in sample["results"]:
                        if result["result_type"] == "tdr_snapshot":
                            snapshot_id = result["result_value"]

                            print("------Getting content of snapshot------")
                            content_response = get_snapshot(
                                session=auth_session,
                                snapshot_id=snapshot_id,
                            )

                            print(json.dumps(content_response))
                            for snapshot_content in content_response["result"]:
                                if snapshot_content.get('pass_fail_value'):
                                    print(
                                        f"==>results value is {snapshot_content['pass_fail_value']}"
                                    )
                                print(
                                    f"==>sample id is {snapshot_content['collaborator_sample_id']}"
                                )

                                if snapshot_content.get("technical_report"):
                                    print(
                                        f"==>Tech Report path is {snapshot_content['technical_report']}"
                                    )
                                    print("------drs data for Tech Report------")

                                    retrieve_report_field_content(snapshot_content["technical_report"], session=auth_session)

                                if snapshot_content.get("indication_based_report"):
                                    print(
                                        f"==>Indication Report path is {snapshot_content['indication_based_report']}"
                                    )
                                    print("------drs data for Indication Report------")

                                    retrieve_report_field_content(snapshot_content["indication_based_report"], session=auth_session)

                                if snapshot_content.get("panel_report"):
                                    print(
                                        f"==>Panel Report path is {snapshot_content['panel_report']}"
                                    )
                                    print("------drs data for Panel Report------")

                                    retrieve_report_field_content(report_index=snapshot_content["panel_report"], session=auth_session)
