# Get Metadata for project and test

from common.obtain_token import obtain_session


def get_metadata_for_test_by_project(project_key, test_code, session):
    """
     This function gets test metadata by project and returns the response.

    Args:
        project_key: The project key pf the project the test is in.
        test_code: The code of test you want the metadata of.
        session: The session in which the order will be created. If no session is given, then
                 one will be obtained in the function.

    Returns:
        The gpo response which will contain the test metadata.
    """
    local_session = obtain_session() if not session else session
    submitter_email = "FILL_IN"
    headers = {
        "Actor-Email": submitter_email,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "bcl-example",
    }
    res = local_session.get(
        f"https://gpo-staging.broadinstitute.org/api/catalog/metadata/project/{project_key}/test/{test_code}",
        headers=headers,
    )
    res.raise_for_status()
    return res


if __name__ == "__main__":

    # Key of the project and test you want
    test_code = "FILL_IN"
    project_key = "FILL_IN"

    response = get_metadata_for_test_by_project(
        project_key=project_key, test_code=test_code
    )
    print(response.json())
