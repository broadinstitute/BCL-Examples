# Get order information

from common.obtain_token import obtain_session

# Key of the order you want to get


def retrieve_gpo_order(email: str, order_key: str, session):
    """
     This function gets an order in gpo and returns the response.

    Args:
        email: The email of the user who is creating the order.
        order_key: The key of the order you would like to get.
        session: The session in which the order will be created. If no session is given, then
                 one will be obtained in the function.

    Returns:
        The gpo response which will contain the order information.
    """

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
    """
     This function gets all orders under a project in gpo and returns the response.

    Args:
        email: The email of the user who is creating the order.
        project_key: The key of the project you would like to get the orders from.
        session: The session in which the order will be created. If no session is given, then
                 one will be obtained in the function.

    Returns:
        The gpo response which will contain a list of the orders and their information.
    """

    local_session = obtain_session() if not session else session

    headers = {
        "Actor-Email": email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = local_session.get(
        f"https://gpo-staging.broadinstitute.org/api/order?project_key={project_key}",
        headers=headers,
    )
    res.raise_for_status()
    return res


if __name__ == "__main__":

    order_key = "FILL_IN"
    submitter_email = "FILL_IN"

    response = retrieve_gpo_order(email=submitter_email, order_key=order_key)
    print(response.json())
