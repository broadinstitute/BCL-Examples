# Get Metadata for project and test

from obtain_token import obtain_session

# Key of the project and test you want
test_code = "FILL_IN"
project_key = "FILL_IN"

session = obtain_session()
submitter_email = "FILL_IN"
headers = {
    "Actor-Email": submitter_email,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "bcl-example",
}
res = session.get(
    f"https://gpo-staging.broadinstitute.org/api/catalog/metadata/project/{project_key}/test/{test_code}",
    headers=headers,
)
res.raise_for_status()
print(res.json())
