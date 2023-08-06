import json

from vaknl_gcp import Scheduler
from vaknl_gcp.Scheduler import SchedulerClient

scheduler_client = SchedulerClient(project='sfmc-connector')

p = json.dumps({"data_extension_name": "test_All_Subscribers",
                "project": "sfmc-connector",
                "dataset": "test",
                "table_name": "test_All_Subscribers"})

scheduler_client.create_schedule(Scheduler.HTTP(
    name='TESTAA',
    payload=p,
    url='https://test.nl',
    description='test',
    cron='5 4 * 1 *'
))
