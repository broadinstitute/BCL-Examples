# Use dev endpoint to update sample status

from common.obtain_token import obtain_session


def update_sample_status(order_key, sample_ids:list[str], test_code, email, session):
    global headers, res
    payload = {
        "sidr_order_key": order_key,
        "sidr_sample_ids": sample_ids,
        "test_code": test_code,
        "passing_samples": True,
        "extras": {"status": "FILL_IN", "reason": "FILL_IN"},
        "action": "change_status",
    }
    local_session = obtain_session() if not session else session
    submitter_email = email
    headers = {
        "Actor-Email": submitter_email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = local_session.patch(
        f"https://gpo-staging.broadinstitute.org/dev/sample", json=payload, headers=headers
    )
    res.raise_for_status()
    return res


# Payload to fill in
response = update_sample_status(order_key="FILL_IN", sample_ids=["FILL_IN"], test_code="FILL_IN",
                                email="FILL_IN")
print(response.json())
