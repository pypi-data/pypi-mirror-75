"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IVideoService
from ndlapi.api._pyproto import MultiFrameEmotionService_pb2_grpc as mm_pb2
from ndlapi.api._services.FaceDetectorService import FaceDetectorService as fd


class MultiModalEmotionRecognitionService(IVideoService):
    name = 'MultiModalEmotionRecognition'
    short_name = 'mm'
    stub_cls = mm_pb2.MultiFrameEmotionStub
    media_types = ['video']

    @staticmethod
    def _postprocess_result(old_result):
        faces = fd._postprocess_result(old_result)
        ids = {n: dict(ii)['FaceClustering'] for n, ii in old_result.items()}
        emotions = {n: dict(ii)['MultiModalEmotionsDetector'] for n, ii in old_result.items()}

        for image_key, image_faces in faces.items():
            for face_num, face_id in enumerate(ids[image_key]):
                if face_id != -1 and face_id in dict(emotions[image_key]):
                    faces[image_key][face_num]['emotions'] = dict(emotions[image_key])[face_id]
                else:
                    faces[image_key][face_num]['emotions'] = None

        return faces
