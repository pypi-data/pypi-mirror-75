"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import json
import os
import os.path as osp
from time import localtime


def check_folder(folder):
    try:
        os.mkdir(folder)
    except:
        pass
    finally:
        if not osp.exists(folder):
            raise IOError("Cannot create folder %s" % folder)


def check_extension(video_path=None, image_path=None):
    if video_path is not None:
        return video_path.split('.')[-1].lower() in ('mp4', 'avi', 'webm')
    if image_path is not None:
        return image_path.split('.')[-1].lower() in ('jpeg', 'jpg', 'png')


def save_results(result, path):
    with open(path, 'w') as f:
        json.dump(result, f, indent=2)
    print("\nResults saved to %s" % path)


def parse_image_folders(image_folders):
    def parse_folder(folder):
        paths = []
        for path in os.listdir(folder):
            abs_path = osp.join(folder, path)
            if osp.isdir(abs_path):
                paths.extend(parse_folder(abs_path))
            elif check_extension(image_path=abs_path):
                paths.append(abs_path)
        return paths

    image_paths = []
    for image_folder in image_folders:
        image_paths.extend(parse_folder(image_folder))
    return image_paths


def current_time_str():
    t = localtime()
    return "%02d.%02d.%02d_%02d:%02d:%02d" % (t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)
