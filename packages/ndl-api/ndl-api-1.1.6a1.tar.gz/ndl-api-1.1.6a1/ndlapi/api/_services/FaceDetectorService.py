"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import FaceDetectionService_pb2_grpc as fd_grpc


class FaceDetectorService(IImagesService, IStreamingService, IVideoService):
    name = 'FaceDetector'
    short_name = 'fd'
    stub_cls = fd_grpc.FaceDetectionStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = {n: dict(ii)['FaceDetector'] for n, ii in old_result.items()}
        new_result = {n: [{k: f[k] for k in ('x', 'y', 'w', 'h')} for f in im_faces] for n, im_faces in faces.items()}
        return new_result
