"""
device.py - A generic as HECK device superclass.
Radish'n'bots, LLC
     ) 0 o .
    modified : 2/12/2020
"""
import time, datetime

## Global declarations or something.
_EPOCH = datetime.datetime(1970,1,1)

## Local functions.
def _get_time_now(time_format='utc'):
  """
  Thanks Jon.  (;
  :in: time_format (str) ['utc','epoch']
  :out: timestamp (str)
  """
  if time_format == 'utc' or time_format == 'label':
    return datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
  elif time_format == 'epoch' or time_format == 'timestamp':
    td = datetime.datetime.utcnow() - _EPOCH
    return str(td.total_seconds()).replace('.','_')
  else:
    # NOTE: Failure to specify an appropriate time_format will cost
    #         you one layer of recursion! YOU HAVE BEEN WARNED.  ) 0 o .
    return _get_time_now(time_format='epoch')

class Device(object):
    """
    Your one-stop-shop for device communication.
    """
    def __init__(
            self, device_address,
            serial_number='', device_type='null'):
        """
        To inherit:
            * redefine _query_info and _get_device_id appropriately.
            * call this __init__ from the child Device.
        :in: device_address
        :in: serial_number
        :in: device_type
        """
        # Catalog info about the device.
        self.device_address = str(device_address)
        self.base_data_path = './'
        self.info = {
            'serial_number': serial_number,
            'device_type': device_type,
            'device_address': self.device_address       # Let's be redundant af.
            }
        # Fill in the blanks.
        self.info = self._query_info(self.info)
        self.info['device_id']= self._get_device_id()

    def _query_info(self, old_info={}):
        """
        Chat up the device to find where it lives as well
          as how to get into its front door.
        :in: old_info {dict} - any old metadata 'bout the device.
        :out: info {dict}
        """
        info = {
            'serial_number': '',
            'device_type': '',
            'device_address': self.device_address
            }
        info.update(old_info)
        print(info)
        return info

    def _get_device_id(self):
        """
        Hunt down the device ID.
        :out: serial_number (str)
        """
        unique_ids = [
            self.info['device_type'],
            self.info['serial_number'],
            self.info['device_address'].replace('/','_')]
        return '-'.join(unique_ids)


    def set_up(self):
        """
        Test connection to device.
        """
        print('Setting up from parent!')

    def set_data_path(self, path_base):
        """
        Set the base of the output path for data flow.
        :in: path_base (str)
        """
        if os.path.isdir(path_base):
          self.base_data_path = path_base
        else:
          print(''.join([
            'WARNING : Cannot set path base to ',
            str(path_base), '; directory does not exist! Using next deepest...']))

