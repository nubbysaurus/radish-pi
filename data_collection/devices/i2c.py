"""
i2c_device.py - Wrap your I2C devices up nicely in Python.
Radish'n'bots, LLC
     ) 0 o .
    modified : 2/10/2020
"""
import sys
if sys.version_info[0] < 3:
    print('Alas! I2C unsupported with this Pi below Python3!  ) 0 o .')
    sys.exit(1)
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
import adafruit_ads1x15.analog_in import AnalogIn

class ADS1115(object):
    """
    Wrapper for ADS1115 ADC.
    """
    def __init__(self):
        self.ads = ADS.ADS1115(i2c)

if __name__ == '__main__':
    print('Under construction...  ) 0 o .')
