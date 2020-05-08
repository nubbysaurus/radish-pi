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
import Adafruit_ADS1x15
#import board
#import busio
#i2c = busio.I2C(board.SCL, board.SDA)
#import adafruit_ads1x15.ads1115 as ADS
#from adafruit_ads1x15.analog_in import AnalogIn
try:
    import queue as Queue
    from .sensor import Sensor, __SUPPORTED_EVENTS
except ImportError:
    import Queue
    from sensor import Sensor, __SUPPORTED_EVENTS
except:
    print('):')
    sys.exit()

# states.
[
        _SLEEPING,
        _CONNECTING,
        _SETTING_UP,
        _RUNNING,
        _DISCONNECTING] = range(5)
_CURRENT_DEVICE_STATE = _SLEEPING       # Stay present
_NEXT_DEVICE_STATE = _SLEEPING          #  with eyes on the road.    ) 0 o .
# ADC stuff.
_DEFAULT_ADC_GAIN = 1
_DEFAULT_ADC_DATA_RATE = 128


## Module-definitions.
class ADS1115(Sensor):
    """
    Wrapper for ADS1115 ADC.
    """
    def __init__(self, label, address, interface='i2c'):
        self.f_sample = 2.0
        self.T_sample = 1 / self.f_sample
        try:
            super().__init__(label, address, interface)
        except:
            super(ADS1115, self).__init__(label, address, interface)

    def _fill_info(self):
        """
        Chat up the device to find where it lives as well
          as how to get into its front door.
        :in: old_info {dict} - any old metadata 'bout the device.
        :out: info {dict}
        """
        try:
            super()._fill_info()
        except:
            super(ADS1115, self)._fill_info()
        self.info.update({'class': 'adc'})

    def _get_device_id(self, label):
        """
        See that sensor.
        :in: label (int) Unique id
        :out: id (str)
        """
        # 'sensor' if not redefined.
        return '-'.join(['ads1115',str(label)])

    def set_file_paths(self, path_base='./test_data/'):
        """
        Set the base path to use to direct output data flow.
        :in: path_base (str) working directory [default './test_data/']
        :out: new_path_base (str) 
        """
        _data_extension = 'csv'        # csv
        # Check that base directory exists.
        if not os.path.isdir(path_base):
            say('Creating '+path_base)
            os.mkdir(path_base)
        # Generate unique id a la timestamp.
        timestamp_label = _get_time_now('label')
        new_path_base = '_'.join([
                path_base+timestamp_label,
                self.id])
        self._metadata_path = new_path_base+'_metadata.json'        # TODO: add to usb_camera.
        self._data_path = '.'.join([
            new_path_base,
            _data_extension])

    def _test_sub_channel(self, sub_channel):
        """
        Make sure that sub channel can be read.
        """
        # TODO: add conditionals based on DEVICE_STATE.
        _prev_value = 0
        _reps_to_fail = 30      # How many times a read value is repeated before failing.
        _reps = 0               # Gimme some more reps.
        while 1<2:
            _value = 0
            #try:
            _value = self.channel.read_adc(sub_channel, gain=_DEFAULT_ADC_GAIN, data_rate=_DEFAULT_ADC_DATA_RATE)
            #except:
            #    # TODO
            #    return False
            if _value != _prev_value:
                time.sleep(self.T_sample)
                _reps += 1
                if _reps >= _reps_to_fail:
                    return False
            return True

    def _find_sub_channels(self):
        # TODO: build out Channel/SubChannel ADTs.
        self._sub_channels = []             # Clear sub-channels first.
            for sub_channel in range(4):
                if self._test_sub_channel(self, sub_channel):
                    self._sub_channels.append(sub_channel)

    def _open_connection(self):
        """
        Thread to build an I2C bridge.
        """
        # Attempt to connect to main channel.
        attempt = 1
        while self.state == 'connecting':
            self.channel = Adafruit_ADS1x15.ADS1115(self.address, self.bus)
            if self._test_connection():
                event = (0, 'connected')
                self._post_event(event)
                break
            say(str(self)+' : connection attempt '+str(attempt)+' failure', 'warning')
            attempt += 1

        # Find available ADC channels.
        self._find_sub_channels()
    
    def _test_connection(self):
        """
        Check yer I2C port.
        :out: available (Bool) is device ready for communication?
        """
        # TODO: make fully funky.
        for sub_channel in self._sub_channels:
            if self.channel.read_adc(sub_channel, gain=_DEFAULT_ADC_GAIN):
                return True
        return False

    def _connect(self, (this_priority, this_event)):
        """
        Connect to a camera over OpenCV.
        * Set a timeout using self._set_timeout()!
        """
        global _CONNECTION_TIMER, _CONNECTION_TIMEOUT
        if this_event == 'init':
            say('Connecting to '+str(self))
            self._start_thread(self._open_connection, 'connecting')
            self._set_timer(_CONNECTION_TIMER, _CONNECTION_TIMEOUT)
        elif this_event == 'connected':
            say(str(self)+' : connection established', 'success')
            self.migrate_state('standing_by')
        elif this_event == 'timeout_'+str(_CONNECTION_TIMER):
            say(str(self)+' : timeout connecting to '+str(self)+'; disconnecting', 'warning')
            self.migrate_state('disconnecting')
        else:
            time.sleep(0.1)

    def _stream(self, (this_priority, this_event)):
        """
        Streaming for a preset time.
        """
        global _STREAM_TIMER
        if this_event == 'init':
            say(str(self)+' : stream opening')
            self._start_thread(self._run_stream, 'streaming')
        elif this_event == 'timeout_'+str(_STREAM_TIMER) or this_event == 'stop_received':
            say(str(self)+' : closing stream')
            self.stream = False
        elif this_event == 'stream_stopped':
            say(str(self)+' : stream closed', 'success')
            self.migrate_state('standing_by')
        elif this_event == 'disconnect_received' or this_event == 'disconnected':
            say(str(self)+' : stream interrupted; attempting to disconnect', 'warning')
            self.stream = False
            self.migrate_state('disconnecting')
        else:
            time.sleep(0.1)

    def _stand_by(self, (this_priority, this_event)):
        """
        Idling about.
        """
        if this_event == 'init':
            say(str(self)+' : standing by for input')
        elif this_event == 'stream_received':
            self.migrate_state('streaming')
        elif this_event == 'disconnect_received':
            self.migrate_state('disconnecting')
        else:
            time.sleep(0.1)

    def _disconnect(self, (this_priority, this_event)):
        """
        Disconnecting.
        """
        if this_event == 'init' or this_event == 'timeout_1':
            say(str(self)+' disconnecting')
            self.channel.release()
            cv2.destroyAllWindows() # <-- make sure that you can get rid of this.
            if not self.channel.isOpened():
                self.migrate_state('sleeping')
        else:
            time.sleep(0.1)

    ## state machine
    def wait_for_(self, state):
        """
        Wait for this to be in some state.
        :in: state (str)
        """
        while 1<2:
            if self.state == state:
                break

    def _run(self):
        """
        Check for events, update state broh.
        """
        _migrate_state(CONNECTING)      # Initialy hiding asleep.
        while True:
            new_event = self._get_event()
            if self.state == SLEEPING:
                self._sleep(new_event)
            elif self.state == CONNECTING:
                self._connect(new_event)
            elif self.state == STANDING_BY:
                self._stand_by(new_event)
            elif self.state == STREAMING:
                self._stream(new_event)
            elif self.state == DISCONNECTING:
                self._disconnect(new_event)
            else:
                say(' '.join([
                    'SABLEYE : Device',
                    str(self),
                    'lost; disconnecting'], 'warning')
                self._migrate_state(DISCONNECTING)
            self._update()

    def set_up(self,options={}):
        """
        Setup an ADC.
        :out: success (Bool)
        :in: options {}
        """
        if not self.state == 'sleeping':
            say('Attempting to set up an existing device.', 'warning')
        say('Setting up')
        event = (1, 'connect_received')
        self._post_event(event)

    def clean_up(self):
        """
        Close down shop.
        :out: success (Bool)
        """
        if not self.state == 'sleeping':
            say('Shutting down '+str(self))
            event = (1, 'disconnect_received')
            self._post_event(event)
        else:
            say('Already shut down', 'success')
        
            else:
                time.sleep(0.1)

    def start_recording(self, duration=0.0):
        """
        Turn it on.
        :in: duration (float) streaming time [s]; duration <= 0.0 == continuous streaming!!
        """
        # TODO: Add state check.
        if duration <= 0.0:
            self._stream_mode = 'continuous'
        else:
            self._stream_mode = 'timed'
            self._stream_duration = duration

        event = (1, 'stream_received')
        self._post_event(event)

    def stop_recording(self):
        """
        Turn it off.
        """
        # TODO: Add state check.
        event = (1, 'stop_received')
        self._post_event(event)


def test_adc():
    """
    Ensure that all systems are a big GO.    ) 0 o .
    """
    # Edit overall test duration (s):
    test_duration = 60
    # Sample data from I2C sensors over the desired time frame.
    this_dude = ADS1115('nublord', 0x48)
    #print(this_dude.channel.value, this_dude.channel.voltage)

if __name__ == '__main__':
    print('Under construction...  ) 0 o .')
    test_adc()
