# Vaknl-gcp
Package for working with dataclasses and Google cloud instances as Bigquery and Storage. 
For this to work the dataclasses need to contain only basic python variables as: str, int, dict, list etc. 

## Prerequisites
These modules dependant on the environment variable GOOGLE_CLOUD_PROJECT a.k.a. gcp project id. 

## Bigquery

#### query(query):
Execute query and log errors
```
returns query_job
```

#### stream_to_bigquery(objects: list, table_ref):
Cast python objects to json and stream them to GBQ
Note: this is more expensive compared to using buckets but also quicker

```
returns table ref
```

#### write_disposition_bucket(table_ref, blob_name, write_disposition):
Get data from bucket to GBQ using a write_disposition method

Requires: bucket with name storage_to_bigquery-[project-id] 

- WRITE_DISPOSITION_UNSPECIFIED	Unknown.
- WRITE_EMPTY	This job should only be writing to empty tables.
- WRITE_TRUNCATE	This job will truncate table data and write from the beginning.
- WRITE_APPEND	This job will append to a table.

```
returns load_job.result 
```

## Storage
Requires: bucket with name storage_to_bigquery-[project-id] 

#### def storage_to_bigquery(objects: list, table_ref, write_disposition):
Function that stores data into multiple storage blobs. Afterwards these wil be composed into one storage blob
The reason for this process is to downsize the sie of the data send to Google Cloud Storage.

```
Args:
    objects: dataclasses to process
    table_ref: dataset_name.table_name
    write_disposition: how to write to google bigquery
    batch_size: row size blobs will be created in google storage before they are composed and send to bigquery
    objects_name: name of the them objects stored in storage 
```

#### batch_storage_to_bigquery(self, objects: list, table_ref, write_disposition, finished: bool = True, batch_size=5000, objects_name=None):

Function that stores data into multiple storage blobs. If finished these wil be composed into one storage blob.
The reason for this process is to downsize the sie of the data send to Google Cloud Storage.

```
Args:
    objects: dataclasses to process
    table_ref: dataset_name.table_name
    write_disposition: how to write to google bigquery
    finished: triggers composing all the blobs and storing them in one procedure
    batch_size: row size blobs will be created in google storage before they are composed and send to bigquery
    objects_name: name of the them objects stored in storage
```

#### single_storage_to_bigquery(object, table_ref, write_disposition, batch_size=500, object_name=None):
Function that stores data into a storage blob. Then check if there are more than the batch_size. 
If so it will compose similar blobs and send them to google bigquery.
The reason for this process is to not stream single rows of data into bigquery but wait until there are more and than send them together.
  
```
Args:            
    object: dataclass
    table_ref: dataset_name.table_name
    write_disposition: how to write to google bigquery
    batch_size: how many blobs until composing and sending to google bigquery
    object_name: name of the them object stored in storage 
```

#### list_blobs_with_prefix(bucket_name, prefix, delimiter=None):):
```
Lists all the blobs in the bucket that begin with the prefix.

This can be used to list all blobs in a "folder", e.g. "public/".

The delimiter argument can be used to restrict the results to only the
"files" in the given "folder". Without the delimiter, the entire tree under
the prefix is returned. For example, given these blobs:

    a/1.txt
    a/b/2.txt

If you just specify prefix = 'a', you'll get back:

    a/1.txt
    a/b/2.txt

However, if you specify prefix='a' and delimiter='/', you'll get back:

    a/1.txt

Additionally, the same request will return blobs.prefixes populated with:

    a/b/

Args:
    bucket_name: bucket_name
    prefix: string
    delimiter: string

Return:
    list: blobs
```


## Tasks

#### create_basic_task(url, queue, payload, task_name=None, in_seconds=None):
```
Creates a task that will be placed in a queue

Arg:
    url: url link like http://example.nl/
    queue: name of queue
    payload: dict
    task_name: str
    in_seconds: int

Returns:
    A :class:`~google.cloud.tasks_v2.types.Task` instance.
```

## Scheduler

#### get_schedulers():
Gets back all schedulers form a gcp project
```
returns list[Schedule]
```

#### create_schedule(schedule:Schedule):
Creates a new Schedule
```
Arg: 
    schedule: class: `vaknl-gcp.Scheduler.Schedule`
 
Returns:
    A :class:`~google.cloud.scheduler_v1.types.Job` instance.
```

#### delete_schedule(name:str):
Deletes a schedule
```
Arg:
    name: str name of the schedule

Returns:
    A :class:`~google.cloud.scheduler_v1.types.Job` instance.
```

## Secrets (beta)

#### get_default_secret(secret_id):
```
returns json
```
