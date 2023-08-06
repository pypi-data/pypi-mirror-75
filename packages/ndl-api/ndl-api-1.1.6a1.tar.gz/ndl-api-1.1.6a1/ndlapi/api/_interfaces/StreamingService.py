"""
NeurodataLab LLC 18.11.2019
Created by Andrey Belyaev
"""
from multiprocessing import Event
from ndlapi.api._interfaces.RecognitionService import IRService
from ndlapi.api._pyproto import api_common_pb2 as ac


class IStreamingService(IRService, object):
    def __init__(self, auth):
        super(IStreamingService, self).__init__(auth)
        self.media_types.append('stream')

        self._streaming_function = None
        self._streaming_data_type = None
        self._stop_send_event = Event()
        self._stop_send_event.clear()

    def set_streaming_function(self, streaming_function, data_type):
        assert data_type in ('image', 'bytes')
        self._streaming_function = streaming_function
        self._streaming_data_type = data_type

    def _create_streaming_iterator(self):
        for n, data in enumerate(self._streaming_function()):
            if self._streaming_data_type == 'image':
                import cv2
                data = cv2.imencode('.jpg', data)[1].tobytes()
            yield ac.PackProcessingRequest(pack_data=[ac.BytesData(pack_num=n + 1, data=data)])

            if self._stop_send_event.is_set():
                print('Streaming stopping normally')
                break

    def process_stream(self):
        assert self._streaming_function is not None, "You have to set streaming function first"

        response_iterator = self.stub.process_images_stream(self._create_streaming_iterator())

        for response in response_iterator:
            if response.code == ac.TicketStatusCode.Queued:
                yield ac.TicketStatusCode.Queued, None, 'There are no free workers, please wait'

            elif response.code == ac.TicketStatusCode.InProgress:
                yield ac.TicketStatusCode.InProgress, response.result, ''

            elif response.code == ac.TicketStatusCode.OK:
                yield ac.TicketStatusCode.OK, None, "Streaming end succesfully"
                self._stop_send_event.set()

            else:
                self._stop_send_event.set()
                yield self._process_bad_answer(response)
                break
