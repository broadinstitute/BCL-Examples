# Create and order

from obtain_token import obtain_session

# Example CWGS Order to fill in
cwgs_payload = {
    "project_key": "SDPR-STAGING-X0000X",
    "clinician": {
        "clinician_npi": "[FILL IN]",
        "first_name": "[FILL IN]",
        "last_name": "[FILL IN]",
    },
    "clinical_order_attestation": True,
    "tests": [{"test_code": "C_WGS", "samples": ["[FILL IN]"]}],
    "samples": [
        {
            "metadata": [
                {"key": "collection_date", "value": ["2024-05-07"]},
                {"key": "state_of_collection", "value": ["MA"]},
            ],
            "sample_id": "[FILL IN]",
            "client_barcode": "[FILL IN]",
            "patient": {
                "metadata": [
                    {"key": "first_name", "value": ["Olga"]},
                    {"key": "last_name", "value": ["Deckow"]},
                    {"key": "sex_at_birth", "value": ["M"]},
                    {"key": "state_of_residence", "value": ["MA"]},
                    {"key": "date_of_birth", "value": ["1973-05-07"]},
                ],
                "patient_id": "[FILL IN]",
            },
            "material_type": "WHOLE_BLOOD_WHOLE_BLOOD_FROZEN",
        }
    ],
    "number_of_samples": "1",
}

session = obtain_session()
submitter_email = "FILL_IN"
headers = {
    "Actor-Email": submitter_email,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "bcl-example",
}
res = session.post(
    "https://gpo-staging.broadinstitute.org/api/order",
    json=cwgs_payload,
    headers=headers,
)
res.raise_for_status()
print(res.json())
