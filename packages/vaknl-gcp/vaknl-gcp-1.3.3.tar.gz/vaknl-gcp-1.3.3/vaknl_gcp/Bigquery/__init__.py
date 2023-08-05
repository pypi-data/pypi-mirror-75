"""Extra functions for Google Cloud Bigquery"""

__author__ = "Wytze Bruinsma"

import json
import logging
from google.cloud import bigquery
from google.cloud.bigquery import Client

from vaknl_gcp.DataClasses import rec_to_json


class BigqueryClient(Client):

    def __init__(self, project, **kwargs):
        self.project = project
        super().__init__(project=project, **kwargs)

    def query(self, query):
        """
        Execute query and log errors
        """
        query_job = super().query(query)
        logging.info(f'EXECUTE QUERY: {query}'.rstrip())
        if query_job.errors:
            logging.warning(f'QUERY: {query} ERROR:{query_job.errors}'.rstrip())
            assert False, f'QUERY: {query} ERROR:{query_job.errors}'.rstrip()
        return query_job

    def stream_to_bigquery(self, objects: list, table_ref):
        """
        Cast python objects to json and stream them to GBQ
        Note: this is more expensive compared to using buckets but also quicker
        """
        batch_size = 2000
        table = super().get_table(table=table_ref)

        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            json_batch = list(map(lambda x: json.loads(json.dumps(rec_to_json(x))), batch))
            error = super().insert_rows_json(table=table, json_rows=json_batch)
            if error:
                logging.warning(error)
                assert False, error

    def write_disposition_bucket(self, table_ref, blob_name, write_disposition):
        """
        Get data from bucket to GBQ using a write_disposition method

        WRITE_DISPOSITION_UNSPECIFIED	Unknown.
        WRITE_EMPTY	This job should only be writing to empty tables.
        WRITE_TRUNCATE	This job will truncate table data and write from the beginning.
        WRITE_APPEND	This job will append to a table.
        """
        job_config = bigquery.LoadJobConfig()
        job_config.schema = super().get_table(table_ref).schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = write_disposition

        uri = f'gs://storage_to_bigquery-{self.project}/{blob_name}'
        logging.info(
            f'STORAGE TO GBQ - method: {write_disposition}, blob name: {blob_name}, destination: {table_ref}'.rstrip())
        load_job = super().load_table_from_uri(
            uri,
            destination=table_ref,
            location="EU",  # Location must match that of the destination dataset.
            job_config=job_config
        )  # API request

        load_job.result()
