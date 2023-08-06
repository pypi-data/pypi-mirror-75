"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import grpc
from ndlapi.api._pyproto import api_common_pb2 as ac
from enum import Enum, unique

@unique
class TaskStatus(Enum):
    Undefined = 0
    Progress = 1
    Done = 2
    Stopped = 3
    Error = 4
    Queued = 5


class TaskResult:
    status = TaskStatus.Undefined
    result = {}
    error_message = ""


class IRService:
    name = 'AbstractService'
    short_name = 'as'
    stub_cls = None
    media_types = []
    _unhandled_error_message = """
There is an unhandled error in grpc.
status: {status}, details: {details}
This error may be produced if:
  *  You have wrong key to connect to the server. Generate new one and try again
  *  Something really bad happens with our server. If generating a new keys doesn't help, please let us know
    """

    def __init__(self, auth):
        ssl_cred = grpc.ssl_channel_credentials(auth.ssl_credentials().ca(),
                                                auth.ssl_credentials().key(),
                                                auth.ssl_credentials().cert())

        token_cred = grpc.access_token_call_credentials(auth.token())

        channel_cred = grpc.composite_channel_credentials(ssl_cred, token_cred)
        self.channel = grpc.secure_channel(auth.host(), channel_cred,
                                           options=[('grpc.max_send_message_length', -1),
                                                    ('grpc.max_receive_message_length', -1)])

        self.stub = self.stub_cls(self.channel)

    def _process_bad_answer(self, response) -> TaskResult:
        task_result = TaskResult()
        task_result.error_message = response.msg
        
        if response.code == ac.TicketStatusCode.Stopped:
            task_result.status = TaskStatus.Stopped
            print("Your task had been stopped", response.msg)

        elif response.code == ac.TicketStatusCode.Failed:
            task_result.status = TaskStatus.Error
            print("\nTask error", response.msg)
            print("\nThere is an error while processing video")
            print("If this error produced while processing, it means we have some problems on server")
            print("If his error was produced before processing than "
                  "your key doesn't have permission to use service {}".format(self.name))
            print("Please, generate new key with right permissions and try again")

        elif response.code == ac.TicketStatusCode.Unknown:
            task_result.status = TaskStatus.Undefined
            print("\nThere is an unhandled error while processing video", response.msg)
            print("If so, please let us know.")

        return task_result

    def _handle_error(self, error):
        raise Exception(self._unhandled_error_message.format(status=error.code(), details=error.details()))
