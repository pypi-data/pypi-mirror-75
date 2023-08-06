# Kloudio Python Library

- API version: BETA

The Kloudio Python library provides convinient access to the Kloudio API from Python applications. It can be configured with a on-premise database or a kloudio database.

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

```sh
pip install kloudio
```
(you may need to run `pip` with root permission: `sudo pip install kloudio`)

Then import the package:
```python
import kloudio
```

```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function

import time
import kloudio
from kloudio.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = kloudio.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: bearer
configuration = kloudio.Configuration(
    host = "http://localhost",
    api_key = {
        'bearer': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['bearer'] = 'Bearer'


# Enter a context with an instance of the API client
with kloudio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kloudio.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | 

    try:
        # Clone a connection
        api_response = api_instance.clone_connection(connection_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ConnectionsApi->clone_connection: %s\n" % e)
    
```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ConnectionsApi* | [**clone_connection**](docs/ConnectionsApi.md#clone_connection) | **POST** /v1/connections/{connection_id} | Clone a connection
*ConnectionsApi* | [**create_connection**](docs/ConnectionsApi.md#create_connection) | **POST** /v1/connections | Create a connection
*ConnectionsApi* | [**delete_connection**](docs/ConnectionsApi.md#delete_connection) | **DELETE** /v1/connections/{connection_id} | Delete a connection
*ConnectionsApi* | [**retrieve_connection**](docs/ConnectionsApi.md#retrieve_connection) | **GET** /v1/connections/{connection_id} | Get a connection
*ConnectionsApi* | [**retrieve_connections**](docs/ConnectionsApi.md#retrieve_connections) | **GET** /v1/connections | Get all connections
*ConnectionsApi* | [**share_connection**](docs/ConnectionsApi.md#share_connection) | **POST** /v1/connections/share/{connection_id} | Share a connection
*ConnectionsApi* | [**update_connection**](docs/ConnectionsApi.md#update_connection) | **PUT** /v1/connections/{connection_id} | Update a connection
*JobsApi* | [**create_job**](docs/JobsApi.md#create_job) | **POST** /v1/jobs | Create a job
*JobsApi* | [**delete_job**](docs/JobsApi.md#delete_job) | **DELETE** /v1/jobs/{job_id} | Delete a job
*JobsApi* | [**disable_job**](docs/JobsApi.md#disable_job) | **POST** /v1/jobs/{job_id}/disable | Disable a job
*JobsApi* | [**enable_job**](docs/JobsApi.md#enable_job) | **POST** /v1/jobs/{job_id}/enable | Enable a job
*JobsApi* | [**resume_jobs**](docs/JobsApi.md#resume_jobs) | **POST** /v1/jobs/resume | Resume jobs
*JobsApi* | [**retrieve_job**](docs/JobsApi.md#retrieve_job) | **GET** /v1/jobs/{job_id} | Get a job
*JobsApi* | [**retrieve_jobs**](docs/JobsApi.md#retrieve_jobs) | **GET** /v1/jobs | Get all jobs
*JobsApi* | [**run_job**](docs/JobsApi.md#run_job) | **POST** /v1/jobs/{job_id}/run | Run a job
*JobsApi* | [**suspend_jobs**](docs/JobsApi.md#suspend_jobs) | **POST** /v1/jobs/suspend | Suspend jobs
*JobsApi* | [**update_job**](docs/JobsApi.md#update_job) | **PUT** /v1/jobs | Update a job
*LicenseApi* | [**create_license**](docs/LicenseApi.md#create_license) | **POST** /v1/license | Create a license
*LicenseApi* | [**delete_license**](docs/LicenseApi.md#delete_license) | **DELETE** /v1/license/{license_id} | Delete a license
*LicenseApi* | [**get_licenses**](docs/LicenseApi.md#get_licenses) | **GET** /v1/license | Get all licenses
*LicenseApi* | [**update_license**](docs/LicenseApi.md#update_license) | **PUT** /v1/license | Update a license
*RegisterApi* | [**register_user**](docs/RegisterApi.md#register_user) | **POST** /v1/register | Register a user
*ReportsApi* | [**create_report**](docs/ReportsApi.md#create_report) | **POST** /v1/reports | Create a report
*ReportsApi* | [**delete_report**](docs/ReportsApi.md#delete_report) | **DELETE** /v1/reports/{report_id} | Delete a report
*ReportsApi* | [**execute_report**](docs/ReportsApi.md#execute_report) | **POST** /v1/reports/{report_id}/execute | Execute a report
*ReportsApi* | [**get_report**](docs/ReportsApi.md#get_report) | **GET** /v1/reports/{report_id} | Get a report
*ReportsApi* | [**get_reports**](docs/ReportsApi.md#get_reports) | **GET** /v1/reports | Get all report
*ReportsApi* | [**share_report**](docs/ReportsApi.md#share_report) | **POST** /v1/reports/share/{report_id} | Share a report
*ReportsApi* | [**update_report**](docs/ReportsApi.md#update_report) | **PUT** /v1/reports/{report_id} | Update a report


## Documentation For Models

 - [ConnectionDelResponse](docs/ConnectionDelResponse.md)
 - [ConnectionRespose](docs/ConnectionRespose.md)
 - [ConnectionShareResponse](docs/ConnectionShareResponse.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [JobsArray](docs/JobsArray.md)
 - [NewConnection](docs/NewConnection.md)
 - [NewJob](docs/NewJob.md)
 - [NewLicense](docs/NewLicense.md)
 - [NewReport](docs/NewReport.md)
 - [NewUser](docs/NewUser.md)
 - [ReportDelResponse](docs/ReportDelResponse.md)
 - [ReportShareResponse](docs/ReportShareResponse.md)
 - [ReportsResponse](docs/ReportsResponse.md)
 - [RunReport](docs/RunReport.md)
 - [ShareConnection](docs/ShareConnection.md)
 - [ShareReport](docs/ShareReport.md)
 - [UpdateConnection](docs/UpdateConnection.md)
 - [UpdateLicense](docs/UpdateLicense.md)


## Documentation For Authorization


## bearer

- **Type**: API key
- **API key parameter name**: api-key
- **Location**: HTTP header


## Author




