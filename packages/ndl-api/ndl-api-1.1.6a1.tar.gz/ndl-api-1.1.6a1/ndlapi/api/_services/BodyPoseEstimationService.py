"""
NeurodataLab LLC 05.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IImagesService, IStreamingService, IVideoService
from ndlapi.api._pyproto import BodyTrackerService_pb2_grpc as bp_grpc


class BodyPoseEstimationService(IImagesService, IStreamingService, IVideoService):
    name = 'BodyPose'
    short_name = 'bp'
    stub_cls = bp_grpc.BodyTrackerStub
    media_types = ['images', 'video']

    @staticmethod
    def _postprocess_result(old_result):
        new_result = {}
        for image_key, image_info in old_result.items():
            bt_info = dict(image_info)['BodyTracker']
            new_result[image_key] = [{i: {'x': p[0], 'y': p[1], 'confidence': p[2]} if p is not None else None
                                      for i, p in enumerate(points_info)} for points_info in bt_info]
        return new_result
