"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IVideoService
from ndlapi.api._pyproto import HeartRateService_pb2_grpc as hr_grpc
from ndlapi.api._services.FaceDetectorService import FaceDetectorService as fd


class HeartRateService(IVideoService):
    name = 'HeartRate'
    short_name = 'hr'
    stub_cls = hr_grpc.HeartRateDetectorStub
    media_types = ['video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = fd._postprocess_result(old_result)
        hr = {n: dict(ii)['HeartRateEstimator'] for n, ii in old_result.items()}
        res = {}

        for image_key, image_hr_info in hr.items():
            try:
                face = faces[image_key][int(image_hr_info['face_num'])]
                face['hr'] = image_hr_info['hr']
                res[image_key] = face
            except:
                res[image_key] = None

        return res
