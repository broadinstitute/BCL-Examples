# Use dev endpoint to update sample status

from common.obtain_token import obtain_session


def update_sample_status(order_key, sample_ids: list[str], test_code, email, status, session=None):
    """
     This function updates the statuses of samples in gpo utlilizing the dev endpoint.

    Args:
        order_key: The key of the order that has the samples to be updated.
        sample_ids: A list of strings containing the id's of the samples to be updated.
        test_code: The code of test you want to update the samples of.
        email: The email of the user who is updating the samples.
        status: The desired new status for the sample(s) passed in
        session: The session in which the order will be created. If no session is given, then
                 one will be obtained in the function.

    Returns:
        The gpo response for updating samples which contains an array of the changes.
    """
    global headers, res
    payload = {
        "sidr_order_key": order_key,
        "sidr_sample_ids": sample_ids,
        "test_code": test_code,
        "passing_samples": True,
        "extras": {"status": status, "reason": "FILL_IN"},
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
        f"https://gpo-staging.broadinstitute.org/dev/sample",
        json=payload,
        headers=headers,
    )
    res.raise_for_status()
    return res


if __name__ == "__main__":
    # Payload to fill in
    response = update_sample_status(order_key="FILL_IN", sample_ids=["FILL_IN"], test_code="FILL_IN", email="FILL_IN",
                                    status="[FILL_IN]")
    print(response.json())
