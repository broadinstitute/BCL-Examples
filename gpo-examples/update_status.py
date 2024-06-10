# Use dev endpoint to update sample status

from common.obtain_token import obtain_session

# Payload to fill in
payload = {
    "sidr_order_key": "FILL_IN",
    "sidr_sample_ids": ["FILL_IN"],
    "test_code": "FILL_IN",
    "passing_samples": True,
    "extras": {"status": "FILL_IN", "reason": "FILL_IN"},
    "action": "change_status",
}

session = obtain_session()
submitter_email = "FILL_IN"
headers = {
    "Actor-Email": submitter_email,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "bcl-example",
}
res = session.patch(
    f"https://gpo-staging.broadinstitute.org/dev/sample", json=payload, headers=headers
)
res.raise_for_status()
print(res.json())
