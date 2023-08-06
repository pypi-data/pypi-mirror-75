"""
NeurodataLab LLC 12.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._interfaces import IVideoService
from ndlapi.api._pyproto import BreathTrackerService_pb2_grpc as brt_grpc


class BreathTrackerService(IVideoService):
    name = 'BreathTracker'
    short_name = 'brt'
    stub_cls = brt_grpc.BreathTrackerStub
    media_types = ['video']

    @staticmethod
    def _postprocess_result(old_result):
        try:
            last_frame_key = sorted(list(old_result.keys()), key=int)[-1]
            breath_frames = list(map(int, dict(old_result[last_frame_key])['BreathTracker']))

            result = {k: True if int(k) in breath_frames else False for k in old_result.keys()}
        except BaseException as e:
            result = old_result
        return result
