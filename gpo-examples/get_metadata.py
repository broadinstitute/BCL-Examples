# Get Metadata for project and test

from common.obtain_token import obtain_session

# Key of the project and test you want
test_code = "FILL_IN"
project_key = "FILL_IN"


def get_metadata_for_test_by_project(project_key=project_key, test_code=test_code):
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
    return res


response = get_metadata_for_test_by_project(project_key=project_key, test_code=test_code)
print(response.json())
