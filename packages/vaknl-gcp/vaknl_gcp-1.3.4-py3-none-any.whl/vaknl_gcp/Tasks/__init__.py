"""Extra functions for Google Cloud Tasks"""

__author__ = "Wytze Bruinsma"


from datetime import datetime, timedelta
from google.cloud.tasks_v2 import CloudTasksClient
from google.protobuf import timestamp_pb2


class TaskClient(CloudTasksClient):

    def __init__(self, project, location='europe-west1'):
        self.project = project
        self.location = location
        super().__init__()

    def create_basic_task(self, url, queue, payload, task_name=None, in_seconds=None):
        """
        Creates a task that will be placed in a queue

        Arg:
            url: url link like http://example.nl/
            queue: name of queue
            payload: dict
            task_name: str
            in_seconds: int

        Returns:
            A :class:`~google.cloud.tasks_v2.types.Task` instance.
        """

        # Construct the fully qualified queue name.
        parent = super().queue_path(self.project, self.location, queue)

        # Construct the request body.
        task = {
            'http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'url': url  # The full url path that the task will be sent to.
            }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['http_request']['body'] = converted_payload

        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.utcnow() + timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp

        if task_name is not None:
            # Add the name to tasks.
            task['name'] = task_name

        # Use the client to build and send the task.
        response = super().create_task(parent, task)

        print('Created task {}'.format(response.name))
        return response
