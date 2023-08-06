from dataclasses import dataclass

from vaknl_gcp.Scheduler.Schedule import Schedule


@dataclass
class PubSub(Schedule):
    """
    Child class from Schedule contains the pub sub version
    """

    topic_name: str

    def asdict(self, base_name, project):
        return {
            "name": f'{base_name}{self.name}',
            "description": self.description,
            "pubsub_target": {
                "topic_name": f"projects/{project}/topics/{self.topic_name}",
                "data": self.payload.encode()
            },
            "schedule": self.cron,
            "time_zone": "Europe/Amsterdam"
        }
