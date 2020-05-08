"""
yellowpages.py - YOU CANNOT HIDE YOUR SHNEEF.
    last modified: 11/12/2019
     ) 0 o .
"""
__version__ = "0.1"

import os
import sys
import time
import glob
import subprocess as sp

import argparse
import datetime
#import cv2

# GLOBAL JUNK
#devnull = open(os.devnull, 'wr')

def fill_yellowpages():
  """
  Poll for all devices visible.
  :output yp: {}
  """
  yp = {}
  # Poll for all available devices.
  find_stuff = [
    'find /sys/bus/usb/devices/usb*/'
  ]
  finder = sp.Popen(
    find_stuff,
    shell=True,
    stdout=sp.PIPE,
    stderr=sp.PIPE
  )
  _buff_available_devices, _errors = finder.communicate(timeout=15)
  available_devices = _buff_available_devices.decode('utf-8').split('\n')
  
  # Check each device for info.
  check_stuff = 'udevadm info -q property --export -p '
  for device in available_devices:
    check_device = [check_stuff+device]
    checker = sp.Popen(
      check_device,
      shell=True,
      stdout=sp.PIPE,
      stderr=sp.PIPE
    )
    _buff_device_info, _errors = checker.communicate(timeout=5)
    device_info = _buff_device_info.decode('utf-8').split('\n')
    yp[device] = {}
    for field in device_info:
      try:
        label, value = field.split('=')
      except:
        continue
      value = value.replace('\'', '')
      prompt = device+' - '+label+' : '+value
      yp[device][label] = value
#      if field.find('DRIVER')!=-1:
#        yp[device]['driver'] = driver
        
#  for thing in yp.keys():
#    try:
#      print(str(yp[thing]['driver']))
#    except:
#      pass
  print(str(yp))
  return yp

def get_yellowpages():
  """
  Get info.
  :output yp: {}
  """
  yp = fill_yellowpages()
  return yp

def infotron(args):
  """
  YOUR DEVICES SHALL BE MINE, STARCHILD!
  :input args: {dict}
  """
  things = get_yellowpages()
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
  infotron(args)
