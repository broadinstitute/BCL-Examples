# Get order information

from common.obtain_token import obtain_session

# Key of the order you want to get


def retrieve_gpo_order(email: str, order_key: str):
    session = obtain_session()
    headers = {
        "Actor-Email": email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = session.get(
        f"https://gpo-staging.broadinstitute.org/api/order/{order_key}", headers=headers
    )
    res.raise_for_status()
    return res


order_key = "FILL_IN"
submitter_email = "FILL_IN"

response = retrieve_gpo_order(email=submitter_email, order_key=order_key)
print(response.json())
