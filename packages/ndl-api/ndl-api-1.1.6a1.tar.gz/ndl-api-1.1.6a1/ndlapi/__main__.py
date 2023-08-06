"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import os

try:
    _trows, _tcols = list(map(int, os.popen('stty size', 'r').read().split()))
except:
    _trows, _tcols = 50, 50

_description = """
Neurodata Lab Tools for processing media data via API.

For video processing run
$ python3 -m ndlapi.process_video
             --keys-path KEYS_PATH 
             --service SERVICE_NAME 
             --video-path VIDEO_PATH 
             --result-path RESULT_PATH

For image processing run
$ python3 -m ndlapi.process_images 
             --keys-path KEYS_PATH
             --service SERVICE_NAME 
             --image-paths [IMAGE_PATH, ...]
             --image-folders [IMAGE_FOLDER, ...]
             --result-path RESULT_PATH

For print help run
$ python3 -m ndlapi.process_video --help
$ python3 -m ndlapi.process_images --help

For detailed manual visit api.neurodatalab.dev/docs 
{}
""".format('-' * min(_tcols, 55))

print(_description)
