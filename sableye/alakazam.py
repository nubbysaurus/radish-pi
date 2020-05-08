"""
alakazam.py - Feel da magic algo-rhythms.
modified : 5/7/2020
     ) 0 o .
"""
import copy, random, datetime


## Helper functions.
def _check_wrist(time_format='utc'):
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
    else:
        # NOTE: Failure to specify an appropriate time_format will cost
        #         you one layer of recursion! YOU HAVE BEEN WARNED.  ) 0 o .
        return _check_wrist(time_format='epoch')


class Node(object):
    """
    Kinda binary tree node here.
    """
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

        # Useful aliases.
        self.value = key

    def __str__(self):
        return str(self.key)

## PriorityEvent-level defs for y'all.
_MIN_PRIORITY = 2       # Priority is inversive!!1?!.
_MAX_PRIORITY = 0
class PriorityEvent(Node):
    """
    :in: label (str)
    """
    def __init__(self, label, priority=_LOWEST_PRIORITY):
        self.time_created = _check_wrist('utc')
        self.time_raised = None
        self.label = str(label)
        self.info = {}
        if event_type:
            self.type = event_type
        else:
            self.type = str(label)
        try:
            super().__init__(priority)
        except:
            super(PriorityEvent, self).__init__(priority)

    def __str__(self):
        return str(self.label)

    def __int__(self):
        # Priority is set to int(self)
        return int(self.priority)

    # Useful alias.
    self.priority = self.value

def set_priority_range(lowest=2, highest=0):
    global _MIN_PRIORITY, _MAX_PRIORITY
    _MIN_PRIORITY, _MAX_PRIORITY = lowest, highest


def _shift_vacancy(them_nodes, current_index, value):
    vacant = current_index
    node_location = 0
    while vacant > 0:
        if them_nodes[vacant-1].key <= value:
            node_location = vacant
            break
        them_nodes[vacant] = them_nodes[vacant-1]
        vacant -= 1
    return node_location


## Module definitions.
def insertion_sort(them_nodes):
    """
    Insertion sort for ADTs with keys.
    REQUIRED: ADT has 'key' method.
    """
    # TODO: build out Event class.
    n = len(them_nodes)
    for index in range(0,n):
        to_sort = copy.deepcopy(them_nodes[index])
        value = to_sort.key
        new_index = _shift_vacancy(them_nodes, index, value)
        them_nodes[new_index] = to_sort
    return

## Algo tests.
def __test_shift_vacancy(them_nodes, current_index, value, operations=0):
    vacant = current_index
    node_location = 0
    while vacant > 0:
        operations += 1
        if them_nodes[vacant-1].key <= value:
            node_location = vacant
            break
        them_nodes[vacant] = them_nodes[vacant-1]
        vacant -= 1
    return node_location, operations

def _test_insertion_sort(them_nodes):
    """
    TEST: Insertion sort for ADTs with keys.
    REQUIRED: ADT has 'key' method.
    """
    operations = 0
    # TODO: build out Event class.
    n = len(them_nodes)
    for index in range(0,n):
        operations += 1
        to_sort = copy.deepcopy(them_nodes[index])
        value = to_sort.key
        new_index, operations = __test_shift_vacancy(them_nodes, index, value, operations)
        them_nodes[new_index] = to_sort
    return operations

def _generate_random_nodes(val_range, n):
    """
    :in: val_range (int, int)
    :in: n (int)
    """
    random_nodes = []
    for i in range(0,n):
        random_nodes.append(Node(random.randint(val_range[0], val_range[1])))
    return random_nodes

def _test_sorting():
    """
    Compare sorting algorithms with large arrays of integers.
    """
    to_sort = _generate_random_nodes((0,9), 50)
    _is_operations = _test_insertion_sort(copy.deepcopy(to_sort))
    print('Insertion sort : '+str(_is_operations))

## yUseful aliases.
sort = insertion_sort   # <-- Change this for efficiency
sortNumerically = sort

## Tests.
if __name__ == "__main__":
    _test_sorting()
