"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import argparse
import os
import os.path as osp
from ndlapi.api import check_connection, create_credentials, get_service_by_name, images_services_list, utils


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
  * PersonDetector ( PersonDetector | pd )

For detailed manual visit api.neurodatalab.dev/docs 
    or run python3 -m ndlapi.process_images --help
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
                        help='Service to process video. Available services: %s' % str(images_services_list))
    parser.add_argument('--image-paths', type=str, nargs='+', default=(),
                        help='Paths to images for process')
    parser.add_argument('--image-folders', type=str, nargs='+', default=(),
                        help='Paths to folders with images for process')
    parser.add_argument('--result-path', type=str, default=default_values['result_path'],
                        help='Path to folder for save results. Default: %s' % default_values['result_path'])

    # DEBUG ARGS
    parser.add_argument('--api-url', type=str, default=default_values['api_url'], help=argparse.SUPPRESS)
    parser.add_argument('--api-port', type=str, default=default_values['api_port'], help=argparse.SUPPRESS)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()
    assert len(args.image_paths) > 0 or len(args.image_folders) > 0, "At least one input image is required"

    check_connection(args.api_url, args.api_port)

    utils.check_folder(folder=args.result_path)

    ssl_auth = create_credentials(args.keys_path, args.api_url, args.api_port)

    service = get_service_by_name(args.service, ssl_auth)

    im_paths = tuple(args.image_paths) + tuple(utils.parse_image_folders(args.image_folders))
    assert len(im_paths) > 0, "At least one input image is required"

    print("Start processing %d images" % len(im_paths))
    processing_ok, result = service.process_images(im_paths)

    if processing_ok:
        utils.save_results(result, path=osp.join(args.result_path,
                                                 '%s_%s_result.json' % (utils.current_time_str(), args.service)))
