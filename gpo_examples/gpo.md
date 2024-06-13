# Gpo Library

 This directory contains utility functions with examples to utilize gpo's functionality

- `create_order.py` conatins code for [creating an order](https://gpo-staging.broadinstitute.org/api/redoc#tag/Orders-and-Samples/operation/post_order_api_order_post) in gpo. 
- `get_metadata.py` contains code for getting the [test metadata by project](https://gpo-staging.broadinstitute.org/api/redoc#tag/Catalogs/operation/get_test_metadata_details_api_catalog_metadata_project__project_key__test__test_code__get).
- `get_order.py` contains code for [getting an order](https://gpo-staging.broadinstitute.org/api/redoc#tag/Orders-and-Samples/operation/get_orders_api_order_get) in gpo.
- `update_status.py` contains code for utilizing the dev endpoint to [update a samples](https://gpo-staging.broadinstitute.org/dev/redoc#operation/patch_test_samples_dev_sample_patch) status in gpo
