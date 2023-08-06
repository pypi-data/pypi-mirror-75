"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import SingleFrameEmotionService_pb2_grpc as sf_grpc
from ndlapi.api._services.FaceDetectorService import FaceDetectorService as fd


class EmotionRecognitionService(IImagesService, IStreamingService, IVideoService):
    name = 'EmotionRecognition'
    short_name = 'er'
    stub_cls = sf_grpc.SingleFrameEmotionStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = fd._postprocess_result(old_result)
        emotions = {n: dict(ii)['SingleFrameEmotionsDetector'] for n, ii in old_result.items()}

        for frame_num, frame_info in faces.items():
            for face_info, emotions_info in zip(frame_info, emotions[frame_num]):
                face_info['emotions'] = emotions_info

        return faces
