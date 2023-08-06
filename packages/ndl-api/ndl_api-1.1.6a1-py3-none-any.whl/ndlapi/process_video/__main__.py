"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import argparse
import os
import os.path as osp
from ndlapi.api import check_connection, create_credentials, get_service_by_name, video_services_list, utils
from ndlapi.api._interfaces.RecognitionService import TaskStatus


try:
    _trows, _tcols = list(map(int, os.popen('stty size', 'r').read().split()))
except:
    _trows, _tcols = 50, 50
_description = """
Neurodata Lab Tools for processing video via API.
You can process video by one of the following service if you have suitable key:
  * Sex and Age Estimation ( SexAge | sa )
  * Body Pose Estimation ( BodyPose | bp )
  * Emotion Recognition ( EmotionRecognition | er )
  * Face Detector ( FaceDetector | fd )
  * MultiModal Emotion Recognition ( MultiModal | mm )
  * Heart Rate ( HeartRate | hr ) 
  * PersonDetector ( PersonDetector | pd )
  * Satisfaction Index ( SatisfactionIndex | si )

For detailed manual visit api.neurodatalab.dev/docs 
    or run python3 -m ndlapi.process_video --help
{}
""".format('-' * min(_tcols, 55))


def parse():
    default_values = {
        'result_path': 'results',
        'api_url': 'ru1.recognition.api.neurodatalab.dev',
        'api_port': '30051'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys-path', required=True, type=str,
                        help='Path to folder with keys downloaded from api.neurodatalab.dev')
    parser.add_argument('--service', required=True, type=str,
                        help='Service to process video. Available services: %s' % str(video_services_list))
    parser.add_argument('--video-path', required=True, type=str,
                        help='Path to video for process')
    parser.add_argument('--result-path', type=str, default=default_values['result_path'],
                        help='Path to folder for save results. Default: %s' % default_values['result_path'])
    parser.add_argument('--api-url', type=str, default=default_values['api_url'], help=argparse.SUPPRESS)
    parser.add_argument('--api-port', type=str, default=default_values['api_port'], help=argparse.SUPPRESS)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    check_connection(args.api_url, args.api_port)

    assert utils.check_extension(video_path=args.video_path), "Video has bad extension"
    utils.check_folder(folder=args.result_path)

    ssl_auth = create_credentials(args.keys_path, args.api_url, args.api_port)

    service = get_service_by_name(args.service, ssl_auth)

    task_result = service.process_video(args.video_path)

    if task_result.status == TaskStatus.Done:
        utils.save_results(task_result.result, path=osp.join(args.result_path,
                                                 '%s_%s_result.json' % (args.video_path.split('/')[-1], args.service)))
