# Get order information

from common.obtain_token import obtain_session

# Key of the order you want to get


def retrieve_gpo_order(email: str, order_key: str, session):

    local_session = obtain_session() if not session else session

    headers = {
        "Actor-Email": email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = local_session.get(
        f"https://gpo-staging.broadinstitute.org/api/order/{order_key}", headers=headers
    )
    res.raise_for_status()
    return res


def retrieve_gpo_orders(email: str, project_key, session):

    local_session = obtain_session() if not session else session

    headers = {
        "Actor-Email": email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = local_session.get(
        f"https://gpo-staging.broadinstitute.org/api/order?project_key={project_key}", headers=headers
    )
    res.raise_for_status()
    return res

if __name__ == "__main__":

    order_key = "FILL_IN"
    submitter_email = "FILL_IN"

    response = retrieve_gpo_order(email=submitter_email, order_key=order_key)
    print(response.json())
