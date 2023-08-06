"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import json
from grpc._channel import _Rendezvous
from queue import Empty
from multiprocessing import Event, Queue
from ndlapi.api._interfaces.RecognitionService import IRService
from ndlapi.api._pyproto import api_common_pb2 as ac
from ndlapi.api._utils import print_progress


class IImagesService(IRService, object):
    def __init__(self, auth):
        super(IImagesService, self).__init__(auth)
        self.media_types.append('images')

    def process_images(self, image_paths):
        def create_stream():
            blob = []
            for im_num, im_path in enumerate(image_paths):
                image_data = open(im_path, 'rb').read()
                blob.append(ac.BytesData(pack_num=im_num, data=image_data))
                if len(blob) == self._streaming_blob_size:
                    yield ac.PackProcessingRequest(pack_data=blob)
                    blob = []

            if len(blob) > 0:
                yield ac.PackProcessingRequest(pack_data=blob)

        processing_ok, result = False, {}
        try:
            response_iterator = self.stub.process_images_stream(create_stream())

            print("Establishing connection ... This may take a while")

            total_images_count, last_done_image_num = len(image_paths), 0.
            for response in response_iterator:
                if response.code == ac.TicketStatusCode.Queued:
                    print('Your response now in queue')

                elif response.code == ac.TicketStatusCode.InProgress:
                    for image_res in response.result:
                        result[image_paths[image_res.num]] = json.loads(image_res.result)
                        last_done_image_num = max(last_done_image_num, image_res.num)

                    print_progress(images_progress={'done': last_done_image_num,
                                                    'total': total_images_count,
                                                    'pct': float(last_done_image_num) / total_images_count})

                elif response.code == ac.TicketStatusCode.OK:
                    processing_ok = True
                    for image_res in response.result:
                        result[image_paths[image_res.num]] = json.loads(image_res.result)

                else:
                    self._process_bad_answer(response)

        except _Rendezvous as e:
            self._handle_error(e)

        else:
            print()
            result = self._postprocess_result(result)

        return processing_ok, result

    @staticmethod
    def _postprocess_result(old_result):
        return old_result
        
    @property
    def _streaming_blob_size(self):
        return 16
