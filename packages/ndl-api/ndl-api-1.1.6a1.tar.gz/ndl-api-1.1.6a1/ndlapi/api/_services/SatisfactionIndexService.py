"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import SatisfactionIndexService_pb2_grpc as si_grpc
from ndlapi.api._services.EmotionRecognitionService import EmotionRecognitionService as er


class SatisfactionIndexService(IImagesService, IStreamingService, IVideoService):
    name = 'SatisfactionIndex'
    short_name = 'si'
    stub_cls = si_grpc.SatisfactionIndexStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        face_emo = er._postprocess_result(old_result)
        si = {n: dict(ii)['SatisfactionIndex'] for n, ii in old_result.items()}
        for image_key, image_info in face_emo.items():
            for face_num, si_val in enumerate(si[image_key]):
                image_info[face_num]['satisfaction_index'] = si_val
        return face_emo
