# Place an order with GPO. Include example payload for a clinical WGS order.

from bcl.auth.obtain_session import obtain_session
from bcl.constants import STAGING_SERVER


def place_gpo_order():
    """
    This function creates an order in gpo with the given payload and returns the response.
    """
    local_session = obtain_session(STAGING_SERVER)

    headers = {
        "Actor-Email": "[FILL_IN]",
    }
    res = local_session.post(
        f"{STAGING_SERVER}/api/order",
        json={
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
        },
        headers=headers,
    )
    res.raise_for_status()
    print(res.json())


if __name__ == "__main__":
    place_gpo_order()
