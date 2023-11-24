# Python Sample

This part of the repository contains Python sample code for quering the RDQM kernel module JSON document.

The code is structured as an API (rdqm/kmod.py) and an application (rdqmkmodquery.py) that calls the API.

There are two main queries that can be run:
1. A query based just on a RHEL kernel version
2. A query based on both a RHEL kernel version and an MQ version

The script `runqueries` contains examples of each query, using the published documents.

The output when this script is run should be:
```
Query 1a: A query for a kernel that is not in the document at all.
python rdqmkmodquery.py 3.10.0-1160.82.1
{
    "kernelVersion": "3.10.0-1160.82.1",
    "note": "kernelVersion has not yet been tested"
}


Query 1e: A query for a kernel that has been fully tested and all MQ VRMFs are compatible.
python rdqmkmodquery.py 4.18.0-477.10.1
{
    "kernelVersion": "4.18.0-477.10.1",
    "status": "Compatible",
    "compatibleMqVRMs": {
        "9.3.0": {
            "testedVrmf": "9.3.0.2",
            "minVrmf": "9.3.0.0",
            "drbdKmod": "kmod-drbd-9.1.12_4.18.0_477.10.1-1"
        },
        "9.2.0": {
            "testedVrmf": "9.2.0.10",
            "minVrmf": "9.2.0.7",
            "drbdKmod": "kmod-drbd-9.1.12_4.18.0_477.10.1-1"
        },
        "9.3.x": {
            "testedVrmf": "9.3.2.0",
            "minVrmf": "9.3.0.0",
            "drbdKmod": "kmod-drbd-9.1.12_4.18.0_477.10.1-1"
        }
    }
}


Query 2e: A query for a kernel that has been fully tested and all MQ VRMFs are compatible, MQ level matches
python rdqmkmodquery.py --mq 9.3.0.1 5.14.0-162.22.2
{
    "kernelVersion": "5.14.0-162.22.2",
    "status": "Compatible",
    "minVrmf": "9.3.0.0",
    "testedVrmf": "9.3.0.2",
    "drbdKmod": "kmod-drbd-9.1.12_5.14.0_162.22.2-1"
}


Query 2f: A query for a kernel that has been fully tested and all MQ VRMFs are compatible, MQ level does not match
python rdqmkmodquery.py --mq 9.2.0.8 5.14.0-162.22.2
{
    "kernelVersion": "5.14.0-162.22.2",
    "status": "Compatible",
    "note": "MQ VRMF is not compatible with RHEL kernel"
}
```

For each query, the command to run the query is given, followed by the results obtained.

## Offline Usage

If you want to run the queries on systems that are not connected to the Internet, you can host your own copies of the JSON document and schema
and execute the queries against either local files or URLs if you host the JSON document and schema on an internal web server for example.

An example query using a local file for both the instance document and the schema document is:
```
python rdqmkmodquery.py --instance_file ibm-mq-rdqm-kmods.json --mq 9.3.4.3 --schema_file ibm-mq-rdqm-kmods.schema.v1-0.json 5.14.0-284.13.3
```

An example query using a local URL for both the instance document and the schema document is:
```
python rdqmkmodquery.py --instance_url http://localhost/ibm-mq-rdqm-kmods.json --mq 9.4.1.1 --schema_url http://localhost/ibm-mq-rdqm-kmods.schema.v1-0.json 5.14.0-284.14.1
```

## Requirements

This code was developed and tested using Python 3.9.18.

To install the required packages using pip, run the command `pip install -r requirements.txt`.
