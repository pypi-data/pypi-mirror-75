#from pyEyeTrack.EyeTracking.BlinkingClass import Blinking

#Bnk = Blinking(0)
#Bnk.start()
import os
import sys
import bz2
import unittest
from functools import partial

from tqdm import tqdm
import dlib

SHAPE_PREDICTOR_FNAME = 'shape_predictor_68_face_landmarks.dat'
SHAPE_PREDICTOR_BZ2_FNAME = SHAPE_PREDICTOR_FNAME + '.bz2'
SHAPE_PREDICTOR_URL = 'http://dlib.net/files/{}'.format(SHAPE_PREDICTOR_BZ2_FNAME)

SHAPE_PREDICTOR_FNAME = 'ffmpeg-snapshot.tar'
SHAPE_PREDICTOR_BZ2_FNAME = 'ffmpeg-snapshot.tar.bz2'
SHAPE_PREDICTOR_URL = 'https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2'

def _download_file(url, out_path):
    try:
        from urllib import urlretrieve          # Python 2
    except ImportError:
        from urllib.request import urlretrieve  # Python 3

    # Wrap tqdm instance with urlretrieve compatible function
    # Abuse mutable [] argument to give function 'memory'
    # First argument will be supplied using partial (an instance of tqdm)
    def reporthook(t, b=1, bsize=1, tsize=None, last_b=[0]):
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
    
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=out_path) as t:
        urlretrieve(url, filename=out_path, reporthook=partial(reporthook, t))

def _bz2_decompress_inplace(path, out_path):
    with open(path, 'rb') as source, open(out_path, 'wb') as dest:
        dest.write(bz2.decompress(source.read()))


#from urllib.request import urlretrieve

script_path = os.path.dirname(os.path.abspath(__file__))

#print('Downloading {} to ./{}'.format(SHAPE_PREDICTOR_URL,
#                                            SHAPE_PREDICTOR_BZ2_FNAME))

#if os.path.exists(SHAPE_PREDICTOR_FNAME)==False:
    
_download_file(SHAPE_PREDICTOR_URL, SHAPE_PREDICTOR_BZ2_FNAME)
_bz2_decompress_inplace(SHAPE_PREDICTOR_BZ2_FNAME,
                                SHAPE_PREDICTOR_FNAME)

print(script_path)
print(SHAPE_PREDICTOR_FNAME)
print()