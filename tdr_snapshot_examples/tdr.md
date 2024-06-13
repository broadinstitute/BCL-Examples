# Terra Data Repository Library

 This directory contains utility functions with examples to get snapshot and file information from tdr.

- `get_file_info_by_drs_path.py` conatins for getting the data of an uploaded [file using its drs path](https://drshub.dsde-prod.broadinstitute.org/#/drsHub/resolveDrs).
- `get_snapshot_with_drs_and_download.py` contains code executing an end to end example of downloading a file from a snapshot. It first gets the snapshot, then looks at the reports, and then saves the files if there are
 any.
- `get_snpashot.py` contains code for getting an snapshot from tdr.
