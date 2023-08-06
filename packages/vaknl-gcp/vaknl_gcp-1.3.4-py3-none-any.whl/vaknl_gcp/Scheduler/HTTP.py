from dataclasses import dataclass

from vaknl_gcp.Scheduler.Schedule import Schedule


@dataclass
class HTTP(Schedule):
    """
    Child class from Schedule contains the HTTP version
    """
    url: str

    def asdict(self, base_name, project):
        return {
            "name": f'{base_name}{self.name}',
            "description": self.description,
            "http_target": {
                "uri": self.url,
                "http_method": "POST",
                "headers": {
                    "key": "Content-Type",
                    "value": "application/octet-stream",
                },
                "body": self.payload.encode()
            },
            "schedule": self.cron,
            "time_zone": "Europe/Amsterdam"
        }
