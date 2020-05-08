"""
ratata.py - pffft.
     ) 0 o .
"""
import json

def ratata():
    event_index = 1
    event_name_base = 'ratata'
    event_calendar = {}
    _default_event_path = './configs/_default_calendar.json'

    for hour in range(0,24):
        for minute in range(0,60):
            for second in range(0,60,30):
                event_time = ':'.join([
                    "{:0>2d}".format(hour),
                    "{:0>2d}".format(minute),
                    "{:0>2d}".format(second)])
                event_calendar[event_time] = {
                            'event_name': '-'.join([event_name_base,str(event_index)])
                            }
                event_index += 1
    with open(_default_event_path, 'w') as efp:
        json.dump(event_calendar, efp)
 

if __name__ == "__main__":
    ratata()
