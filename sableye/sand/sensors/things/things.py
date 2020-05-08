"""
things.py - Things   ) 0 o .

modified: 1/16/2020
"""
__version__ = "0.1"

# Import the right stuff!
import os, sys, time, argparse, datetime

try:
  import queue
except ImportError:
  import Queue as queue

## Global variables.
_EPOCH = datetime.datetime(1970, 1, 1)

_default = {
    'base_data_path': './'
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


class Device:
  """
  A Thing.   ) 0 o .
  """
  def __init__(self,
               _address,
               _id,
               _base_data_path='./',
               _format='csv'):
    """
    :input _address: (str)
    :input _id: (str)
    """
    self.address = _address
    self.name = _id
    self._format = _format
    self.data_path = ''

    # Data variables and services.
    self._buffer_size = 1024    # Number of data lines to be kept as buffer.
    self.output_buffer = []

    # Initial setup.
    self._active = False
    self._recording = False
    self.set_output_data_path(_base_data_path)

  def _start_thread(self,
                    target,
                    name):
    """
    :input target: (FUNC)
    :input name: (str)
    """
    thread = threading.Thread(
        target=target,
        name=name)

  def set_output_format(self, _format=''):
    """
    Update format of output file.
    """
    self._format = _format

  def set_output_data_path(self, base_data_path=''):
    """
    Set a full output data path.
    """
    timestamp_label = _get_time_now('utc')    # TODO: Check dis
    if not base_data_path:
      base_data_path = _default['base_data_path']
    data_path_fields = [base_data_path, timestamp_label, self.name]
    # Set that path.
    self.data_path = '.'.join(['_'.join(data_path_fields), self._format])

  def _read_line(self):
    """
    Read data if you can! <Device-specific>
    :output data_line: (str)
    """
    data_line = ''
    return data_line

  def _write_data_line(self, data_line):
    """
    Write a line of data.
    :input data_line: (str)
    """
    # TODO: Add optional timestamps
    with open(self.data_path, 'a+') as data_output:
      data_output.write(data_line)


  def _record(self):
    """
    Hear that sweet, sweet data.
    """
    self._recording = True
    while self._recording:
      # Clear the buffer.
      while not self.output_buffer.empty():
        data_line = self.output_buffer[0]
        self._write_data_line(data_line)
        self.output_buffer.pop(0)
        continue
      else:
        time.sleep(0.1)

  def _listen(self):
    """
    The data, She pours!
    """
    self._active = True
    while self._active:
      data = self.read_line()
      if data:
        # Dequeue data as it gets old and crusty.
        if len(output_buffer) >= self._buffer_size:
          self.output_buffer = []
        # ...and stack on that fresh stuff.
        self.output_buffer.append(data)
      else:
        time.sleep(0.1)

  def start_recording(self):
    """
    Stream to a file.
    """
    # 'dreaming' + 'remembering' = recording (q.e.d.)
    needed_threads = {
        'dreaming': self._listen,
        'remembering': self._record}

    # Check if a needed thread is still alive.
    active_threads = threading.enumerate()
    active_thread_names = [thread.name for thread in active_threads]
    for name in needed_threads.keys():
      if name in active_thread_names:
        needed_threads.pop(name)

    # Start up any still needed threads.
    for milk in needed_threads.keys():  # =label
      self._start_thread(
          target=needed_threads[milk],
          name=milk)

  def stop_recording(self):
    """
    Close the gates.
    """
    timeout = 60  # 1min
    self._recording = False
    active_threads = threading.enumerate()
    for thread in active_threads:
      if thread.name == 'remembering':
        thread.join([timeout])
        break

if __name__ == '__main__':
    print('Checking things...')
