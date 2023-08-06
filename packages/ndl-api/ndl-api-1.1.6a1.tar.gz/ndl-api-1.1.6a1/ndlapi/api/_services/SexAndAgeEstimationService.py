"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import AgeEstimationService_pb2_grpc as ae_grpc
from ndlapi.api._services.FaceDetectorService import FaceDetectorService as fd


class SexAndAgeEstimationService(IImagesService, IStreamingService, IVideoService):
    name = 'SexAndAge'
    short_name = 'sa'
    stub_cls = ae_grpc.AgeEstimationStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = fd._postprocess_result(old_result)
        fa = {n: dict(ii)['FaceAttributesDetector'] for n, ii in old_result.items()}
        for image_key, image_info in faces.items():
            for face_num, fa_val in enumerate(fa[image_key]):
                image_info[face_num]['gender'] = fa_val['gender']
                image_info[face_num]['age'] = fa_val['age']
        return faces
