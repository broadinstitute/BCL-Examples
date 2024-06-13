# Gets the report file information based off the provided drs path

import json


def get_file_info_by_drs_path(session, drs_path):
    """
    This function gets file info utilizing the given drs path and then outputs the
    name, uri, and access url before returning the json of the file.

    Args:
        session: The session in which the order will be created. If no session is given, then
                one will be obtained in the function.
        drs_path: The drs path to the file you want the information of.

    Returns:
        The json of the file from the request.
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "GPO Bound Query",
        "Content-Type": "application/json",
        "accept": "*/*",
    }
    drs_response = session.post(
        url="https://drshub.dsde-prod.broadinstitute.org/api/v4/drs/resolve",
        headers=headers,
        data=json.dumps(
            {
                "url": drs_path,
                "fields": [
                    "bucket",
                    "name",
                    "size",
                    "timeCreated",
                    "timeUpdated",
                    "fileName",
                    "accessUrl",
                    "gsUri",
                ],
            }
        ),
    )

    drs_json = drs_response.json()
    print(f"==>file name is {drs_json['fileName']}")
    print(f"==>gsUri is {drs_json['gsUri']}")
    print(f"==> Access Url for downloading is {drs_json['accessUrl']['url']}")
    print(
        f"\n\n To download this on the command line execute \ncurl -X GET -o [path to local file] \"{drs_json['accessUrl']['url']}\"\n\n"
    )

    return drs_json
