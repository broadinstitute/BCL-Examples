from random import random

import click
from faker import Faker

from common.obtain_token import obtain_session
from gpo_examples.create_order import place_gpo_order
from gpo_examples.get_order import retrieve_gpo_order
from gpo_examples.update_status import update_sample_status

payload = {
    "offset": 0,
    "limit": 30,
    "sort": "datarepo_row_id",
    "direction": "asc",
    "filter": "",
}
auth_session = obtain_session()

fake_data = Faker()
fakedate = fake_data.date_between_dates(date_start="-3d", date_end="-2d")
random_base = random()
test_code = "C_WGS"
cwgs_payload = {
    "project_key": "[FILL_IN]",
    "clinician": {
        "clinician_npi": "[FILL_IN]",
        "first_name": "[FILL_IN]",
        "last_name": "[FILL_IN]",
    },
    "clinical_order_attestation": True,
    "tests": [{"test_code": test_code, "samples": [f"{random_base}"]}],
    "samples": [
        {
            "metadata": [
                {"key": "collection_date", "value": [f"{fakedate.isoformat()}"]},
                {"key": "state_of_collection", "value": ["MA"]},
            ],
            "sample_id": f"SM-{random_base}",
            "client_barcode": f"{random_base}",
            "patient": {
                "metadata": [
                    {"key": "first_name", "value": [f"{fake_data.first_name()}"]},
                    {"key": "last_name", "value": [f"{fake_data.last_name()}"]},
                    {"key": "sex_at_birth", "value": ["M"]},
                    {"key": "state_of_residence", "value": ["MA"]},
                    {"key": "date_of_birth", "value": ["1973-05-07"]},
                ],
                "patient_id": f"PT-{random_base}",
            },
            "material_type": "WHOLE_BLOOD_WHOLE_BLOOD_FROZEN",
        }
    ],
    "number_of_samples": "1",
}

submitter = "[FILL_IN]"
placed_order = place_gpo_order(submitter, cwgs_payload, auth_session).json()

order_id = placed_order["order_id"]
click.echo(f"New order placed with order Key of {order_id}")

samples = [sample["sidr_sample_id"] for sample in placed_order["samples"]]
new_status = "RECEIVED"
update_sample_status(
    order_key=order_id,
    sample_ids=samples,
    test_code=test_code,
    email=submitter,
    status=new_status,
    session=auth_session,
)

find_order = retrieve_gpo_order(
    email=submitter, order_key=order_id, session=auth_session
).json()

for test in find_order["tests"]:
    for sample in test["test_samples"]:
        if sample["sidr_sample_id"] in samples:
            assert sample["test_sample_status"] == new_status
            click.echo(
                f"Verified that sample {sample['sidr_sample_id']} had its status modified to {new_status}"
            )
