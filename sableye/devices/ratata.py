"""
ratata.py - Disposable code.
  ) 0 o .

"""
# Imports for testing.
import time
try:
    from alakazam import set_priority_range, sortNumerically, PriorityEvent
except ImportError:
    from .alakazam import set_priority_range, sortNumerically, PriorityEvent
# Global declarations
i = 'mongeese'

# Halpers
def _print(things):
    """
    Print the things.
    """
    print(' '.join(things))


def pooper():
    _default_priorities = [0,1,2]
    _set1_priorities = range(9,0,-1)
    print(str(_set1_priorities))
    _set2_priorities = [87,1,5,3]
    _set3_priorities = [3,2,5,2,5,3,5,0]

    for _priority_numbers in [
            _default_priorities,
            _set2_priorities,
            _set1_priorities,
            _set3_priorities]:
        _priority_min = max(_priority_numbers)
        _priority_max = min(_priority_numbers)
        print('min, max priorities = '+str(_priority_min)+', '+str(_priority_max))
        set_priority_range(_priority_min, _priority_max)

        events = []
        for _label, _priority in enumerate(_priority_numbers):
            new_event = PriorityEvent(_label, _priority)
            print(str(new_event)+' : '+str(int(new_event)))
            events.append(new_event)
        sortNumerically(events)
        for event in events:
            print(str(int(event)))
        time.sleep(2)


# Module-level classes
class Poop():
    def __init__(self):
        i = 'puppies'
        _print([
            'within poop',
            '\ni',
            i])

if __name__ == '__main__':
    pooper()
