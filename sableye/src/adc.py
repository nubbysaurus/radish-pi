import Adafruit_ADS1x15
import time

# Pinout:
#   * SDA - GPIO2
#   * SCL - GPIO3
#   * VDD - +3.3V
#   * GND - 0V

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

# To install this package on the raspberry pi, use:
#
# sudo apt-get update
# sudo apt-get install build-essential python-dev python-smbus python-pip
# sudo pip install adafruit-ads1x15
#
# Additional information available from Adafruit:
# https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115

class ADC():
    def __init__(self, adc_address=0x48, i2c_bus=1):
        self.i2c_bus = i2c_bus             # default: 1 (0 on older pi's)
        self.adc_address = adc_address     # default: 0x48
        self.adc_i = Adafruit_ADS1x15.ADS1115(address=adc_address, busnum=1)
        print("Connected sensor: ADS1115 @ " + str(self.adc_address))

    def readADC(self, adc_pin_address, adc_gain):
        return self.adc_i.read_adc(adc_pin_address, gain=adc_gain)

def milk():
    """
    Test ADCs!
    """
    thing = ADC(adc_address=0x49)
    print('Testing out the ADC.  ) 0 o .')
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
    print('-' * 37)
    while(1<2):
        values = [0]*4
        for index in range(4):
            values[index] = thing.readADC(index, GAIN)
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        time.sleep(0.1)


if __name__ == '__main__':
    milk()
