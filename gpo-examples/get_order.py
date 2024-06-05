# Get order information

from obtain_token import obtain_session

# Key of the order you want to get
order_key = "FILL_IN"

session = obtain_session()
submitter_email = "FILL_IN"
headers = {
    "Actor-Email": submitter_email,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "bcl-example",
}
res = session.get(
    f"https://gpo-staging.broadinstitute.org/api/order/{order_key}", headers=headers
)
res.raise_for_status()
print(res.json())
