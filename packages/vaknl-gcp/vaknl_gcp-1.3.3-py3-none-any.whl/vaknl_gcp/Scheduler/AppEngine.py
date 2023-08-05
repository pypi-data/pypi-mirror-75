from dataclasses import dataclass

from vaknl_gcp.Scheduler.Schedule import Schedule


@dataclass
class AppEngine(Schedule):
    """
    Child class from Schedule contains the App engine version
    """
    relative_uri: str
    service: str = 'default'

    def asdict(self, base_name, project):
        return {
            "name": f'{base_name}{self.name}',
            "description": self.description,
            "app_engine_http_target": {
                "http_method": "POST",
                "app_engine_routing": {
                    "service": self.service,
                    "host": f"{self.service}.{project}.ew.r.appspot.com"
                },
                "relative_uri": self.relative_uri,
                "headers": {
                    "key": "User-Agent",
                    "value": "AppEngine-Google; (+http://code.google.com/appengine)"
                },
                "body": self.payload.encode()
            },
            "schedule": self.cron,
            "time_zone": "Europe/Amsterdam"
        }
