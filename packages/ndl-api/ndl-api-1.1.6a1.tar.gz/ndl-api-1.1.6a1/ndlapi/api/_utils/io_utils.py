"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import sys
from functools import reduce
from ndlapi.api._pyproto import api_common_pb2 as ac

worker_names = {
    ac.WorkerType.bb: 'BboxClustering',
    ac.WorkerType.bt: 'BodyPose',
    ac.WorkerType.fa: 'SexAgeEstimator',
    ac.WorkerType.fc: 'FaceClustering',
    ac.WorkerType.fd: 'FaceDetector',
    ac.WorkerType.fe: 'FaceEmbeddings',
    ac.WorkerType.hr: 'HeartRate',
    ac.WorkerType.mm: 'MultiModalEmotionsRecognition',
    ac.WorkerType.pd: 'PersonDetector',
    ac.WorkerType.si: 'SatisfactionIndex',
    ac.WorkerType.sf: 'EmotionsRecognition',
    ac.WorkerType.brt: 'BreathTracker',
    ac.WorkerType.oed: 'OpenEyesDetector',
}


def read_binary(path):
    with open(path, "rb") as binput:
        return binput.read()


def iterate_over_file_bytes(file_path, blob_size):
    def get_blob():
        return f.read(blob_size)

    with open(file_path, 'rb') as f:
        for blob in iter(get_blob, b''):
            yield blob


def print_progress(units_progress=None, images_progress=None, send_progress=None):
    if units_progress is not None:
        progress = reduce(lambda s, u: s + "%s:%1.3f " % (worker_names[u.worker_type], u.progress), units_progress, '')
        sys.stdout.write('\rCurrent progress - %s' % progress[:-1])
        sys.stdout.flush()

    if images_progress is not None:
        sys.stdout.write('\rDone {done} images from {total} ({pct:.3f}%)'.format(**images_progress))
        sys.stdout.flush()

    if send_progress is not None:
        sys.stdout.write('\rSending video bytes.. {:.3f}MB'.format(send_progress / 1024. ** 2))
        sys.stdout.flush()
