"""
NeurodataLab LLC 12.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import OpenEyesDetectorService_pb2_grpc as oed_grpc
from ndlapi.api._services.FaceDetectorService import FaceDetectorService as fd


class OpenEyesDetectorService(IImagesService, IStreamingService, IVideoService):
    name = 'OpenEyesDetector'
    short_name = 'oed'
    stub_cls = oed_grpc.OpenEyesDetectorStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = fd._postprocess_result(old_result)
        eyes = {n: dict(ii)['OpenEyesDetector'] for n, ii in old_result.items()}

        for frame_num, frame_info in faces.items():
            for face_info, eyes_info in zip(frame_info, eyes[frame_num]):
                face_info['eyes'] = eyes_info

        return faces
