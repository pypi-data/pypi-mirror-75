"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
from ._auth.SSLCredentials import create_credentials
from ._services.BodyPoseEstimationService import BodyPoseEstimationService as _BodyPoseEstimationService
from ._services.BreathTrackerService import BreathTrackerService as _BreathTrackerService
from ._services.EmotionRecognitionService import EmotionRecognitionService as _EmotionsRecognitionService
from ._services.FaceDetectorService import FaceDetectorService as _FaceDetectorService
from ._services.HeartRateService import HeartRateService as _HeartRateService
from ._services.MultiModalEmotionRecognition import MultiModalEmotionRecognitionService as _MultiModalEmotionRecognitionService
from ._services.OpenEyesDetectorService import OpenEyesDetectorService as _OpenEyesDetectorService
from ._services.PersonDetectorService import PersonDetectorService as _PersonDetectorService
from ._services.SatisfactionIndexService import SatisfactionIndexService as _SatisfactionIndexServer
from ._services.SexAndAgeEstimationService import SexAndAgeEstimationService as _SexAndAgeEstimationService
from ._utils import os_utils as utils
from ._utils.error_utils import check_connection

_all_services = [
    _BodyPoseEstimationService,
    _BreathTrackerService,
    _EmotionsRecognitionService,
    _FaceDetectorService,
    _HeartRateService,
    _MultiModalEmotionRecognitionService,
    _OpenEyesDetectorService,
    _PersonDetectorService,
    _SatisfactionIndexServer,
    _SexAndAgeEstimationService
]

_services_by_short_name = {service.short_name: service for service in _all_services}
_services_by_long_name = {service.name: service for service in _all_services}

video_services_list = [service.name for service in _all_services if 'video' in service.media_types]
images_services_list = [service.name for service in _all_services if 'images' in service.media_types]


def get_service_by_name(service_name, auth):
    if service_name in _services_by_short_name:
        return _services_by_short_name[service_name](auth)
    elif service_name in _services_by_long_name:
        return _services_by_long_name[service_name](auth)
    else:
        raise NameError("No service %s available" % service_name)
