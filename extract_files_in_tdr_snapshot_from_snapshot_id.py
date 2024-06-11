import json

import click
from google.auth.compute_engine import IDTokenCredentials

from common.obtain_token import obtain_session
from gpo_examples.get_order import retrieve_gpo_orders, retrieve_gpo_order
from tdr_snapshot_examples.get_file_info_by_drs_path import get_file_info_by_drs_path
from tdr_snapshot_examples.get_snapshot import get_snapshot

tdr_domain = "data.terra.bio"

creds: IDTokenCredentials

payload = {
    "offset": 0,
    "limit": 30,
    "sort": "datarepo_row_id",
    "direction": "asc",
    "filter": "",
}
auth_session = obtain_session()
headers = {"Accept": "application/json", "User-Agent": "GPO Bound Query"}

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
    gpo_response = retrieve_gpo_orders(email="scottmat@broadinstitute.org", project_key=project_key, session=auth_session)
elif order_key:
    gpo_response = retrieve_gpo_order(email="scottmat@broadinstitute.org", order_key=order_key, session=auth_session)

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
                print(f"==> Sample ID is {sample['sample_id']}")
                print(f"==> Vessel Barcode is {sample['client_barcode']}")
                print(f"==> SIDR Sample ID is {sample['sidr_sample_id']}")
                print(f"==> Sample status is {sample['test_sample_status']}")
                for result in sample["results"]:
                    if result["result_type"] == "tdr_snapshot":
                        snapshot_id = result["result_value"]

                        headers.update({"Content-Type": "application/json"})
                        print("------Getting content of snapshot------")
                        content_response = get_snapshot(session=auth_session, payload=payload, headers=headers,
                                                        snapshot_id=snapshot_id)

                        print(json.dumps(content_response))
                        for snapshot_content in content_response["result"]:
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
                                headers.update({"accept": "*/*"})

                                drs_json = get_file_info_by_drs_path(auth_session, snapshot_content["technical_report"])

                                print(f"==>file name is {drs_json['fileName']}")
                                print(f"==>gsUri is {drs_json['gsUri']}")
                                print(
                                    f"==> Access Url for downloading is {drs_json['accessUrl']['url']}"
                                )
                                print(
                                    f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{drs_json['accessUrl']['url']}\"\n\n"
                                )

                            if snapshot_content.get("indication_based_report"):
                                print(
                                    f"==>Indication Report path is {snapshot_content['indication_based_report']}"
                                )
                                print("------drs data for Indication Report------")

                                drs_json = get_file_info_by_drs_path(auth_session, snapshot_content["indication_based_report"])

                                print(f"==>file name is {drs_json['fileName']}")
                                print(f"==>gsUri is {drs_json['gsUri']}")
                                print(
                                    f"==> Access Url for downloading is {drs_json['accessUrl']['url']}"
                                )
                                print(
                                    f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{drs_json['accessUrl']['url']}\" \n\n"
                                )
