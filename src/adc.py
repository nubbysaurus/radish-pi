import Adafruit_ADS1x15
import time

# Pinout:
#   * SDA - GPIO2
#   * SCL - GPIO3
#   * VDD - +5V
#   * GND - 0V
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
        self.adc_i = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        print("Connected sensor: ADS1115 @ " + str(self.adc_address))

    def readADC(self, adc_pin_address, adc_gain):
        return self.adc_i.read_adc(adc_pin_address, adc_gain)

def milk():
    """
    Test ADCs!
    """
    thing = ADC(adc_address=0x49)
    while(1<2):
        for index in range(0:4:1):
            print('. '.join([
                str(index),
                thing.readADC(index,1)]))
        time.sleep(0.1)


if __name__ == '__main__':
    milk()
