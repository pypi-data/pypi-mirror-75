"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import PersonDetectorService_pb2_grpc as pd_grpc


class PersonDetectorService(IImagesService, IStreamingService, IVideoService):
    name = 'PersonDetector'
    short_name = 'pd'
    stub_cls = pd_grpc.PersonDetectorStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        new_result = {n: dict(ii)['PersonDetector'] for n, ii in old_result.items()}
        return new_result
