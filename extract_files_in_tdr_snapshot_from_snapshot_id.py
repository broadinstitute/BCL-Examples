import json
import warnings

import click
import google
from google.auth import impersonated_credentials, jwt
from google.auth.compute_engine import IDTokenCredentials
from google.auth.transport import requests  # type: ignore
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

tdr_domain = "data.terra.bio"

snapshot_uuid = ""

target_audience = click.prompt(
    "Specify the target Audience", default="https://gpo-staging.broadinstitute.org"
)
credentials_type = click.prompt(
    "Specify Credentials source [1 = credentials file, 2 = impersonation]", default=1
)

creds: IDTokenCredentials
match credentials_type:
    case 1:
        credentials_file_path = click.prompt("specify the path to the credentials file")
        creds = service_account.IDTokenCredentials.from_service_account_file(
            filename=credentials_file_path,
            target_audience=target_audience,
        )
    case 2:
        expiry = 3600
        service_account_email = click.prompt("Specify the service account to be used")
        project_id = click.prompt("Specify your Google project ID")

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                "Your application has authenticated using end user credentials from"
                " Google Cloud SDK.",
            )
            user_creds, _ = google.auth.default()

        user_creds.refresh(requests.Request())

        # Ensure the user is authenticated with gcloud
        target_creds = impersonated_credentials.Credentials(
            source_credentials=user_creds,
            target_principal=service_account_email,
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=expiry,
            quota_project_id=project_id,
        )
        target_creds.refresh(requests.Request())

        creds = impersonated_credentials.IDTokenCredentials(
            target_credentials=target_creds,
            target_audience=target_audience,
            include_email=True,
            quota_project_id=project_id,
        )
    case _:
        click.echo("Invalid value entered for credentials type")
        exit()

payload = {
    "offset": 0,
    "limit": 30,
    "sort": "datarepo_row_id",
    "direction": "asc",
    "filter": "",
}
auth_session = AuthorizedSession(creds)
headers = {"Accept": "application/json", "User-Agent": "GPO Bound Query"}

project_key = click.prompt(
    "Enter the BCL Order Project for which you wish to retrieve information."
)
gpo_order_url = (
    f"https://gpo-staging.broadinstitute.org/api/order?project_key={project_key}"
)

# sam_response = auth_session.get(url="https://sam.dsde-prod.broadinstitute.org/api/users/v2/self", headers=headers, data={})
# click.echo(json.dumps(sam_response.json()))

# https://gpo-staging.broadinstitute.org/api/redoc#tag/Orders-and-Samples/operation/get_orders_api_order_get
gpo_response = auth_session.get(url=gpo_order_url, headers=headers, data={})
print(f"Token?  {creds.token}")
out = jwt.decode(creds.token, verify=False)
click.echo(json.dumps(out, indent=2))

print(json.dumps(gpo_response.json()))
gpo_order_json = gpo_response.json()
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
                    snapshot_id = (
                        snapshot_uuid if snapshot_uuid else result["result_value"]
                    )
                    snapshot_url_base = f"https://{tdr_domain}/api/repository/v1/snapshots/{snapshot_id}"

                    headers.update({"Content-Type": "application/json"})
                    print("------Getting content of snapshot------")
                    #  https://data.terra.bio/swagger-ui.html#/snapshots/querySnapshotDataById
                    content_response = auth_session.post(
                        url=snapshot_url_base + "/data/sample",
                        headers=headers,
                        data=json.dumps(payload),
                        timeout=5,
                    )

                    # print(json.dumps(content_response.json()))
                    for snapshot_content in content_response.json()["result"]:
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

                            # https://drshub.dsde-prod.broadinstitute.org/#/drsHub/resolveDrs
                            drs_response = auth_session.post(
                                url="https://drshub.dsde-prod.broadinstitute.org/api/v4/drs/resolve",
                                headers=headers,
                                data=json.dumps(
                                    {
                                        "url": snapshot_content["technical_report"],
                                        "fields": [
                                            "bucket",
                                            "name",
                                            "size",
                                            "timeCreated",
                                            "timeUpdated",
                                            "fileName",
                                            "accessUrl",
                                            "gsUri",
                                        ],
                                    }
                                ),
                                timeout=5,
                            )

                            print(json.dumps(drs_response.json()))
                            drs_json = drs_response.json()
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

                            # https://drshub.dsde-prod.broadinstitute.org/#/drsHub/resolveDrs
                            drs_response = auth_session.post(
                                url="https://drshub.dsde-prod.broadinstitute.org/api/v4/drs/resolve",
                                headers=headers,
                                data=json.dumps(
                                    {
                                        "url": snapshot_content[
                                            "indication_based_report"
                                        ],
                                        "fields": [
                                            "bucket",
                                            "name",
                                            "size",
                                            "timeCreated",
                                            "timeUpdated",
                                            "fileName",
                                            "accessUrl",
                                            "gsUri",
                                        ],
                                    }
                                ),
                                timeout=5,
                            )
                            drs_json = drs_response.json()
                            print(f"==>file name is {drs_json['fileName']}")
                            print(f"==>gsUri is {drs_json['gsUri']}")
                            print(
                                f"==> Access Url for downloading is {drs_json['accessUrl']['url']}"
                            )
                            print(
                                f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{drs_json['accessUrl']['url']}\" \n\n"
                            )
