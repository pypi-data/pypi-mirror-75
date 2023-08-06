"""Extra functions for Google Schedule Client"""

__author__ = "Wytze Bruinsma"

from google.cloud.scheduler_v1 import CloudSchedulerClient

from vaknl_gcp.Scheduler.AppEngine import AppEngine
from vaknl_gcp.Scheduler.HTTP import HTTP
from vaknl_gcp.Scheduler.PubSub import PubSub


class SchedulerClient(CloudSchedulerClient):

    def __init__(self, project, location='europe-west1', **kwargs):
        self.project = project
        self.base_name = f'projects/{project}/locations/{location}/jobs/'
        super().__init__(**kwargs)
        self.parent = super().location_path(project=project, location=location)

    def get_schedulers(self):
        """
        Gets back all schedulers form a gcp project

        Return:
            list[Schedule]
        """

        result = []

        for element in super().list_jobs(self.parent):
            name = element.name.split('/').pop()
            description = element.description
            if element.pubsub_target.topic_name:
                topic_split = element.pubsub_target.topic_name.split('/')
                result.append(PubSub(name=name, cron=element.schedule, description=description,
                                     payload=element.pubsub_target.data.decode(),
                                     topic_name=topic_split[3]))
            elif element.app_engine_http_target.app_engine_routing.service:
                result.append(AppEngine(name=name, cron=element.schedule, description=description,
                                        payload=element.app_engine_http_target.body.decode(),
                                        service=element.app_engine_http_target.app_engine_routing.service,
                                        relative_uri=element.app_engine_http_target.relative_uri))
            else:
                result.append(HTTP(name=name, cron=element.schedule, description=description,
                                   payload=element.http_target.body.decode(), url=element.http_target.uri))

        return result

    def create_schedule(self, schedule):
        """
        Creates a new Schedule

        Arg:
            schedule: class: `vaknl-gcp.Scheduler.Schedule`

        Returns:
            A :class:`~google.cloud.scheduler_v1.types.Job` instance.

        """

        return super().create_job(self.parent, schedule.asdict(self.base_name, self.project))

    def delete_schedule(self, name):
        """
        Deletes a schedule

        Arg:
            name: str name of the schedule

        Returns:
            A :class:`~google.cloud.scheduler_v1.types.Job` instance.
        """
        super().delete_job(name=f'{self.base_name}{name}')
