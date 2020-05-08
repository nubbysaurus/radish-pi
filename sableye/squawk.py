"""
squawk.py - KRAW.
Public:
    * say()
    * ask()
modified: 3/24/20202
  ) 0 o .
"""
import datetime

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
    td = datetime.datetime.utcnow() - datetime.datetime(1970,1,1)
    return str(td.total_seconds()).replace('.','_')
  else:
    # NOTE: Failure to specify an appropriate time_format will cost
    #         you one layer of recursion! YOU HAVE BEEN WARNED.  ) 0 o .
    return _get_time_now(time_format='epoch')

def _query_user(query):
    # Foolishly maintain Python2 compatibility.
    try:
        return str(raw_input(query)).strip()
    except:
        return str(input(query)).strip()

def _ask_bool(prompt):
    """
    Ask USER a Boolean question.
    :in: prompt (str)
    :out: response (bool) - {True / False (default)}
    """
    prompt += ' [y/N] : '
    response = _query_user(prompt).lower()
    if response != 'y':
        return False
    return True

def _format_options(options, default=None):
    """
    Format options for USER query.
    :in: options [?]
    :in: default (?)
    :out: addendum (str)
    """
    addendum = ' ['
    index = 1
    total_options = len(options)
    while (index < total_options):
        addendum = ''.join([
            addendum,
            str(options[index]),
            ', '])
    addendum = ''.join([
        addendum,
        str(options[index+1]),
        '] : '])
    if default:
        addendum += '('+str(default)+' [default]) '
    return addendum


## Public functions.
def say(prompt, flag='status'):
    """
    Local print function.
    :in: prompt (str)
    :in: flag (str) - {status, success, error, warning, misc}
    """
    # TODO: (@nubby) add colors y naht?
    now = _get_time_now('timestamp')
    status = flag.upper()
    addendum = '...'
    if status == 'SUCCESS':
        addendum = '!'
    elif status == 'ERROR':
        addendum = '!'
    elif status == 'WARNING':
        addendum = '.'
    output = ''.join([
        now, ' [',
        status, '] : ',
        prompt,
        addendum])
    print(output)

def ask(prompt, options=[], default='', answer_type=str):
    """
    Ask USER for input.
    :in: prompt (str)
    :in: options [str]
    :in: default (str)
    :in: answer_type <type> - type of response
:    :out: ui (?)
    """
    if answer_type == bool:
        return _ask_bool(prompt)
    if options:
        prompt += _format_options(options, default=default)
    _agnostic_response = _query_user(prompt)
    if not _agnostic_response or _agnostic_response == '\n':
        _agnostic_response = default
    try:
        response = answer_type(_agnostic_response)
    except (TypeError, ValueError) as e:
        say(' '.join([
            'SKRAWW!! <: Types are incompatible :',
            str(type(_agnostic_response)),
            'and',
            str(answer_type),
            '; returning default,',
            str(default)]), 'warning')
        response = answer_type(default)
    return response

# Unit tests.
def _test_ask():
    prompt = 'Hi nub? : '
    options=[]
    default=''
    answer_type=str
    
    answer = ask(prompt, options=options, default=default, answer_type=answer_type)
    print(str(answer))

if __name__ == '__main__':
    _test_ask()