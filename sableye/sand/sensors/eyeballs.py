"""
eyeballs.py - Believing is seeing   ) 0 o .

modified: 1/16/2020
"""
__version__ = "0.1"

# Import the right stuff!
import os, sys, time, argparse, datetime, glob, cv2

try:
    from things.things import Device, _EPOCH
    import Queue as queue
except ImportError:
    from .things.things import Device, _EPOCH
    import queue


# Global declarations.
DEFAULTS = {
    'format': {
        'video': 'mp4',
        'image': 'png'
        },
    'resolutions': {
        '1080p': {
            'width': 1920,
            'height': 1080
            }
        }
    }

def _get_time_now(time_format='epoch'):
  """
  Thanks Jon.  (;
  :input time_format: ['utc', 'epoch']
  """
  if time_format == 'utc':
    return datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S%f")
  elif time_format == 'epoch':
    td = datetime.datetime.utcnow() - _EPOCH
    return td.total_seconds()
  else:
    return _get_time_now(time_format='epoch')

def _get_camera_indices():
    """
    Return a list of available camera numbers.
    :output available_indices: [int]
    """
    index_max = 8
    available_indices = []
    for index in range(0,index_max,1):
        cap = cv2.VideoCapture(index)
        if cap and cap.isOpened():
            available_indices.append(index)
            cap.release()
    return available_indices

def _take_picture(camera_index, image_path='./'):
    """
    Capture an image using the desired camera.
    :input camera_index: (int)
    :input image_path: (str)
    """
    eye = cv2.VideoCapture(camera_index)
    ret, frame = eye.read()

    # Label TODO
    label = 'shrooms'

    # Wink a pic. (;
    wink_timestamp = _get_time_now('utc')
    wink_name = '.'.join([
        ('-'.join([
            image_path+wink_timestamp,
            str(camera_index),
            label])),
        DEFAULTS['format']['image']])
    cv2.imwrite(wink_name, frame)
    print('Pic snapped at : '+wink_name)
    eye.release()

class Eyeball(Device):
  """
  A Device that can see.
  """
  def __init__(self, _address, _id,
      _format=DEFAULTS['format']):
    super(Device, self).__init__(_address, _id, _format)
    # video connect here:

  def _read_line(self):
    """
    Look with your special eyes!
    """
    print('My brand!')
    return

def _get_time_now(time_format='epoch'):
  """
  Thanks Jon.  (;
  :input time_format: ['utc', 'epoch']
  """
  if time_format == 'utc':
    return datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S%f")
  elif time_format == 'epoch':
    td = datetime.datetime.utcnow() - _EPOCH
    return td.total_seconds()
  else:
    return _get_time_now(time_format='epoch')

def _get_videos():
  """
  :output videos: [str] port addresses of stuff that's video
  """

  return []

def _get_serial_devs():
  """
  :
  """
  return []

def get_eyeballs():
  """
  Gather your senses.
  """
  # Initial ball array.
  balls = []
  balls += _get_videos()
  balls += _get_serial_devs()
  return balls

def see(args):
  """
  Look with your special eyes!
  :input args: {args}
  """
  eyes = get_eyeballs()
  while(1<2):
    print('Hi nub.')
    time.sleep(1)
  return

def sift():
  """
  Sift through yer arrgs.
  :output args: {dict}
  """
  parser = argparse.ArgumentParser(description='Look with your special eyes!')
  #parser.add_arguement()
  args = {}
  return args

if __name__ == "__main__":
    args = sift()
    #see(args)
    available_camera_indices = _get_camera_indices()
    _take_picture(max(available_camera_indices))
