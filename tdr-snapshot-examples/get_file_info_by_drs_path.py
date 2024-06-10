# Gets the report file information based off the provided drs path

import json

headers = {
    "Accept": "application/json",
    "User-Agent": "GPO Bound Query",
    "Content-Type": "application/json",
    "accept": "*/*",
}


def get_file_info_by_drs_path(session, drsPath):
    drs_response = session.post(
        url="https://drshub.dsde-prod.broadinstitute.org/api/v4/drs/resolve",
        headers=headers,
        data=json.dumps(
            {
                "url": drsPath,
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
