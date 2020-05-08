"""
snorlax.py - Quaff up that data.
modified : 5/4/2020
     ) 0 o .
"""
# Maintain Python2 compatibility...FOOLISHLY.
import sys, time, copy, json, datetime, threading
try:
    import queue as Queue
    from .sableye import detect, set_up_, record_from_, take_picture_from_, clean_up_
    from .alakazam import PriorityEvent, sortNumerically
    from .squawk import ask, say
except:
    import Queue
    from sableye import detect, set_up_, record_from_, take_picture_from_, clean_up_
    from alakazam import Node, sortNumerically
    from squawk import ask, say


## local important stuff.
# events and event generators.
# TODO : best way?
__SUPPORTED_EVENTS = [
        'NO_EVENT',
        'INIT_EVENT',
        'EXIT_EVENT',
        'COMPLETE_EVENT',
        'TIMEOUT_1_EVENT',
        'TIMEOUT_2_EVENT',
        'SCHEDULED_EVENT',
        'INTERRUPT_EVENT',
        'POKEFLUTE_EVENT'
        ]
EVENT_QUEUE = Queue.Queue()     # TODO : priority
EVENT_SCHEDULE = []
_CURRENT_SCHEDULE_INDEX = 0

__SUPPORTED_INTERRUPTS = []
INTERRUPT_QUEUE = Queue.Queue()

# setting priorities.
_HIGHEST_PRIORITY = 0
_LOWEST_PRIORITY = _HIGHEST_PRIORITY + 3
_DEFAULT_PRIORITY = _HIGHEST_PRIORITY + 1
_SCHEDULE_PRIORITY = _DEFAULT_PRIORITY
_INTERRUPT_PRIORITY = _HIGHEST_PRIORITY

# states.
[SLEEPING,
SETTING_UP,
CALIBRATING,
LUMBERING_ABOUT,
CLEANING_UP] = range(0,5)
CURRENT_STATE = CLEANING_UP     # Stay present
NEXT_STATE = SLEEPING           #  with eyes on the road.    ) 0 o .

# devices.
DEVICES = []

# metadata.
TEST_INFO = {
        'devices': {}
        }

# timers/timeouts (s).
_TIMER_RESET = (False, 0.0)
[_TIMER_1,
_TIMER_2] = range(0,2)
_TIMERS = [
        _TIMER_1,
        _TIMER_2]
_TIMERS_MAX = len(_TIMERS)                      # Number of available timers.
_TIMERS_INIT = [_TIMER_RESET]*_TIMERS_MAX       # Reset state for all timers.
ACTIVE_TIMERS = _TIMERS_INIT
_DEFAULT_TIMEOUT = 60
_SET_UP_TIMEOUT = _DEFAULT_TIMEOUT
_CALIBRATION_TIMEOUT = _DEFAULT_TIMEOUT

# other.
_ACTIVE_THREADS = []
_ACTIVE_PROCESSES = []
_EPOCH = datetime.datetime(1970,1,1)
_MIDNIGHT_SEX = 24 * 60 * 60


## helpers.
def _get_time_now(time_format='utc'):
    """
    Thanks Jon.  (;
    :in: time_format (str) ['utc','epoch']
    :out: timestamp (str)
    """
    if time_format == 'utc' or time_format == 'label':
        return datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    elif time_format == 'epoch' or time_format == 'timestamp':
        td = datetime.datetime.utcnow() - _EPOCH
        return str(td.total_seconds())
    elif time_format == 'sex':
        return _hhmmss_to_int(datetime.datetime.utcnow().strftime("%H:%M:%S"))
    else:
        # NOTE: Failure to specify an appropriate time_format will cost
        #         you one layer of recursion! YOU HAVE BEEN WARNED.  ) 0 o .
        return _get_time_now(time_format='epoch')

def _start_thread(target, name, args=(), kwargs={}):
    """
    Get them wheels turning.
    :in: target (*funk)
    :in: name (str) NOTE : set as daemon process with the word 'daemon' in here.
    :in: args (*)
    :in: kwargs {*}
    :out: thread (Thread)
    """
    global _ACTIVE_THREADS
    thread = threading.Thread(target=target, name=name, args=args, kwargs=kwargs)
    if (name.find('daemon')) != -1:
        thread.daemon = True
    thread.start()
    if thread.isAlive():
        _ACTIVE_THREADS.append(thread)
        return thread
    return None

def _migrate_state(next_state):
    """
    But y even thoh?
    State will be changed if it needs to by the next round through.
    """
    global NEXT_STATE
    NEXT_STATE = next_state
    return

# maths.
def _hhmmss_to_int(hhmmss):
    """
    Translate a time in a given day to an int number of seconds since midnight.
    After a check, you do it twice for twice as nice. (;
    """
    try:
        hours, minutes, seconds = _check_hhmmss_format(hhmmss)
    except:
        return None
    sex_time = seconds + 60 * (minutes + 60 * (hours))
    return sex_time

def _check_hhmmss_format(hhmmss):
    """
    Make sure this is all good.
    :out: [int, int, int] hours, minutes, seconds
    """
    try:
        hms = hhmmss.split(':')
    except TypeError:
        say('Cannot convert; must be in HH:MM(:SS optional) format', 'warning')
        return []
    if len(hms) == 3:
        hour_str, min_str, sec_str = hms
    elif len(hms) == 2:
        hour_str, min_str = hms
        sec_str = '00'
    else:
        say('Cannot convert; must be in HH:MM(:SS optional) format', 'warning')
        return []
    
    [hours,
    minutes,
    seconds] = [int(timepiece) for timepiece in [
        hour_str,
        min_str,
        sec_str]]
    if hours < 24 and minutes < 60 and seconds <60:
        return [hours, minutes, seconds]
    else:
        say('Time entered invalid', 'warning')
        return []
    

# timer stuff.
def _start_timer(timer_number, duration):
    """
    Counting down the HH:MM:SS.
    """
    global ACTIVE_TIMERS
    time_left = duration
    start_time = float(_get_time_now('epoch'))
    ACTIVE_TIMERS[timer_number] = (True, time_left)
    while time_left > 0:
        current_time = float(_get_time_now('epoch'))
        time_left = current_time - start_time
    ACTIVE_TIMERS[timer_number] = _TIMER_RESET

def _reset_timers():
    """
    Reset timers.
    """
    global ACTIVE_TIMERS
    ACTIVE_TIMERS = _TIMERS_INIT

def _get_timer_info( timer_num):
    """
    :in: timer_num (int)
    :out: timer_active, time_left (Bool, float)
    """
    try:
        return active_timers[timer_num]
    except:
        say('Invalid timer number: '+str(timer_num), 'error')
        return (False, -1.0)

def _set_timer(timer_number, duration):
    """
    :in: timer_number (int) [0 -> _TIMER_MAX-1]
    :in: duration (float) [seconds]
    """
    timer_active, time_left = _get_timer_info(timer_number)
    if timer_active or time_left < 0:
        say('Cannot set timeout for timer '+str(timer_number), 'warning')
    say('Timeout : '+str(duration)+'s')
    _start_thread(_start_timer, 'timeout-daemon', args=[timer_number, duration])

## scheduler/interrupts TODO : move outta here?

## event stuff.
class ScheduledEvent(Node):
    """
    :in: label (str)
    """
    def __init__(self, label, event_type='', event_time=''):
        self.time_created = _get_time_now('utc')
        self.time_raised = None
        self.label = str(label)
        if event_type:
            self.type = event_type
        else:
            self.type = str(label)
        if event_time:
            key = _hhmmss_to_int(event_time)
        else:
            key = 0
        try:
            super().__init__(key)
        except:
            super(Event, self).__init__(key)

    def __str__(self):
        return str(self.label)

    def __int__(self):
        return int(self.key)


def _get_event():
    global EVENT_QUEUE, _LOWEST_PRIORITY
    if EVENT_QUEUE.empty():
        no_event = PriorityEvent('NO_EVENT')
        return no_event
    return EVENT_QUEUE.get_nowait()[1]

def _post_event(priority, event_in):
    """
    Post events to the event queue.
    :in: event (str, Event) depending on input, will cast as an Event
    """
    global EVENT_QUEUE
    if type(event_in) != Event:
        event = Event(event_in)     # Input is a string.
    else:       # TODO : this should be mejor.
        event = event_in
    priority_event = priority, event
    EVENT_QUEUE.put_nowait(priority_event)

def _add_to_schedule(event_name, event_time):
    """
    Post events to calendar.
    """
    global EVENT_SCHEDULE
    if not _check_hhmmss_format(event_time):
        event_time = 0
    event = Event(
            event_name,
            event_type='SCHEDULED_EVENT',
            event_time=event_time)
    EVENT_SCHEDULE.append(event)    # TODO : add priority?
    sortNumerically(EVENT_SCHEDULE)

def _clear_events():
    global EVENT_QUEUE
    while not EVENT_QUEUE.empty():
        _get_event()


## file management
def _load_events():
    _event_path_default = './configs/_every30s.json'
    event_path = ask(
            'Event file path : ',
            default=_event_path_default,
            answer_type=str)
    #try:
    with open(event_path, 'r') as efp:
        say('Reading from '+event_path)
        _new_calendar = json.load(efp)
    #except:
    #    say('Event file does not exist; no events pre-loaded', 'warning')
    #    return
    # Parse out each event.
    event_count = 0
    for event_hhmmss in _new_calendar.keys():
        try:
            _add_to_schedule(_new_calendar[event_hhmmss]['event_name'], event_hhmmss)
            event_count += 1
            say(str(event_count)+'. Added '+event_hhmmss)
        except KeyError:
            say('Calendar not properly formatted', 'error')
        except:
            pass
    say('Finished adding events from '+event_path)

## user interface
def _fill_calendar():
    if ask('Load events? : ', answer_type=bool):
        _load_events()
    if ask('Any more events to add to schedule?', answer_type=bool):
        while 1<2:
            prompts = [
                    'Event name : ',
                    'Event time [HH:MM(:SS optional) (UTC)] : ',
                    'Add another event?']
            answer_types = [
                    str,
                    str,
                    bool]
            [event_name,
            event_time,
            add_events] = [ask(prompt, answer_type=answer_types) for prompt, answer_types in zip(prompts, answer_types)]
            _add_to_schedule(
                    event_name,
                    event_time)
            if not add_events:
                break


## state machine
# NOTE : implement as a class?
# TODO : best way?
# meat of the machine.
def _build_test_info(connected_devices=[]):
    global TEST_INFO
    _fill_calendar()
    for device in connected_devices:
        TEST_INFO['devices'][str(device)] = 'hi nublette.'

def _start_set_up():
    """
    Find available devices, ask USER about test, connect to devices.
    """
    # TODO : merge DEVICES and TEST_INFO?
    global TEST_INFO, DEVICES
    DEVICES = detect()
    _build_test_info(connected_devices=DEVICES)
    set_up_(DEVICES)
    _post_event(_DEFAULT_PRIORITY, 'COMPLETE_EVENT')

def _start_calibration():
    # TODO : once devices are all added.
    say('SNORLAX : Calibration complete', 'success')
    _post_event(_DEFAULT_PRIORITY, 'COMPLETE_EVENT')

def _start_clean_up():
    """
    Gently disconnect from devices, ask USER for next moves.
    """
    clean_up_(DEVICES)
    # TODO : (while DEVICES.unclean: sleep mas)
    _post_event(_DEFAULT_PRIORITY, 'COMPLETE_EVENT')

def _hibernation():
    """
    Zzz...
    """
    prompt = 'SNORLAX : Wake with Pokeflute? [Press ENTER]'
    ask(prompt)
    _post_event(_HIGHEST_PRIORITY, 'POKEFLUTE_EVENT')

def _get_lumbering():
    while 1<2:
        #prompt = 'SNORLAX : Take a pic y naht? [Press ENTER, or \'exit\' to quit]'
        #response = ask(prompt)
        #if not response == 'exit':
        #take_picture_from_(DEVICES)
        #    continue
        #_post_event(_DEFAULT_PRIORITY, 'EXIT_EVENT')
        #break
        pass

def _handle_calendar():
    say('Spoon me largely', 'success')
    time.sleep(0.1)
    return

def _handle_interrupt():
    return

# actual machine.
def _get_next_scheduled_event():
    # TODO - make dis better nub.
    _calendar_size = len(EVENT_SCHEDULE)
    _next_event = None
    if _calendar_size > 0:
        _current_sex = _get_time_now('sex')
        for index, event in enumerate(EVENT_SCHEDULE):
            if int(event) >= _current_sex:
                say('Waiting for next event # '+str(index+1)+' of '+str(_calendar_size))
                _next_event = event
                break
    return _next_event

def _start_scheduler():
    next_event = _get_next_scheduled_event()
    while CURRENT_STATE == LUMBERING_ABOUT:
        current_time = _get_time_now('sex')     # TODO : switch to Epoch.
        try:
            if current_time < int(next_event):
                time.sleep(0.4)
                continue
        except:
            time.sleep(1)
            next_event = _get_next_scheduled_event()
            continue

        _post_event(_SCHEDULE_PRIORITY, next_event)
        say('Posted : '+str(next_event))
        time.sleep(1)
        next_event = _get_next_scheduled_event()
        say('Next up : '+str(next_event))
    return

def _check_interrupts():
    return

def _check_devices():
    """
    Just make sure all is proper.
    """
    return

def _check_timers():
    for index, timer in enumerate(ACTIVE_TIMERS):
        if timer[0] and timer[1] < 0:
            event_name = '_'.join([
                'TIMEOUT',
                str(timer),
                'EVENT'])
            _post_event(_HIGHEST_PRIORITY, event_name)

def _update_state():
    global CURRENT_STATE, NEXT_STATE
    if NEXT_STATE != CURRENT_STATE:
        CURRENT_STATE = NEXT_STATE
        _clear_events()
        _reset_timers() # TODO : see if this is all gouda.
        _post_event(_HIGHEST_PRIORITY, 'INIT_EVENT')


def _update():
    #_check_schedule()
    _check_interrupts()
    _check_devices()
    _check_timers()
    _update_state()

def _rest(new_event):
    """
    This needs USER attention to wake up.
    """
    new_event_name = new_event.type
    if new_event_name == 'INIT_EVENT':
        say('SNORLAX : Zzz...')
        _start_thread(_hibernation, 'hibernating-daemon')
    elif new_event_name == 'POKEFLUTE_EVENT':
        _migrate_state(SETTING_UP)
    else:
        time.sleep(0.3)
    return

def _set_up(new_event):
    global DEVICES
    new_event_name = new_event.type
    if new_event_name == 'INIT_EVENT':
        _start_thread(_start_set_up, 'setting_up-daemon')
        _set_timer(_TIMER_1, _SET_UP_TIMEOUT)
    elif new_event_name == 'COMPLETE_EVENT':
        _migrate_state(CALIBRATING)
    elif new_event_name == 'TIMEOUT_1_EVENT':
        _migrate_state(CLEANING_UP)
    else:
        time.sleep(0.1)
    return

def _calibrate(new_event):
    new_event_name = new_event.type
    if new_event_name == 'INIT_EVENT':
        _start_thread(_start_calibration, 'calibrating-daemon')
        _set_timer(_TIMER_1, _CALIBRATION_TIMEOUT)
    elif new_event_name == 'COMPLETE_EVENT':
        _migrate_state(LUMBERING_ABOUT)
    else:
        time.sleep(0.1)
    return

def _lumber_about(new_event):
    new_event_name = new_event.type
    if new_event_name == 'INIT_EVENT':
        _start_thread(_get_lumbering, 'lumbering-daemon')
        _start_thread(_start_scheduler, 'scheduler-daemon')
    elif new_event_name == 'SCHEDULED_EVENT':
        _start_thread(_handle_calendar, 'calendar-daemon')
    elif new_event_name == 'INTERRUPT_EVENT':
        _start_thread(_handle_interrupt, 'interruption-daemon')     # TODO : make priorities of interrupts.
    elif new_event_name == 'EXIT_EVENT':
        _migrate_state(CLEANING_UP)
    elif new_event_name == 'NO_EVENT':
        time.sleep(0.3)
    return

def _clean_up(new_event):
    new_event_name = new_event.type
    if new_event_name == 'INIT_EVENT':
        _start_thread(_start_clean_up, 'cleaning_up-daemon')
        _set_timer(_TIMER_1, _SET_UP_TIMEOUT)
    elif new_event_name == 'COMPLETE_EVENT':
        _migrate_state(SLEEPING)
    else:
        time.sleep(0.1)
    return

def run(user_input):
    """
    Initialize and run test.
    """
    _migrate_state(SETTING_UP)    # Initial state is asleep.
    global CURRENT_STATE
    while 1<2:
        new_event = _get_event()
        if CURRENT_STATE == SLEEPING:
            _rest(new_event)
        elif CURRENT_STATE == SETTING_UP:
            _set_up(new_event)
        elif CURRENT_STATE == CALIBRATING:
            _calibrate(new_event)
        elif CURRENT_STATE == LUMBERING_ABOUT:
            _lumber_about(new_event)
        elif CURRENT_STATE == CLEANING_UP:
            _clean_up(new_event)
        else:
            _migrate_state(CLEANING_UP)
        _update()

def _sift_args():
    """
    Parse out USER arguments into a dictionary.
    :out: user_input {}
    """
    # TODO
    return {}

def snorlax():
    """
    This script manages device interactions and allows USER to define
        testing parameters.
    """
    user_input = _sift_args()
    try:
        run(user_input)
    except KeyboardInterrupt:
        say('SNORLAX : Wild Snorlax fainted!', 'success')
        sys.exit()

if __name__ == "__main__":
    snorlax()
