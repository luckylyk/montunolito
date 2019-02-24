"""
This module contains all generic utils for the montunolito
It's mainly containing utils for array and number offset.
But also utils to choose random elements
"""
import random


def remap_array(array, offset=0, value=10):
    ''' this method remap an array int between 0 and value '''
    return [remap_number(number + offset, value=value) for number in array]


def find_closer_number(reference, array, clamp=11, return_index=False):
    reference = remap_number(reference, clamp)
    array = remap_array(array=array, value=clamp)
    if reference in array:
        return array.index(reference) if return_index else reference

    closer_difference = None
    for i, number in enumerate(array):
        difference = min(
            abs(reference - number), abs(reference + clamp - number))
        if not closer_difference or closer_difference > difference:
            closer_index = i
            closer_difference = difference
    return closer_index if return_index else array[closer_index]


def count_occurence_continuity(array):
    '''
    utils who count the occurence in a list before a difference
    example :
        ['salut', 'salut', 'salut', 'prout', 'salut'] = 3
        ['salut', 'prout', 'salut', 'salut', 'salut'] = 1
    '''
    result = 0
    for element in array:
        if element != array[0]:
            break
        result += 1
    return result


def remap_number(number, value=10):
    ''' this method remap an int between 0 and value '''
    while number > value - 1:
        number -= value
    while number < 0:
        number += value
    return number


def offset_array(array, offset):
    ''' this method offset a list '''
    return array[offset:] + array[:offset - len(array)]


def choose(items):
    '''
    this method is an utils to choose an element with a coefficient.
    :items: is a dict {'item1': coefficien as int}
    return a random key with a chance coefficient as value
    '''
    return random.choice([
        t for k, v in items.items()
        for t in tuple([k] * v) if v])


def replace_in_array(indexes, items, array):
    '''
    place the give items in the given array at the given indexes.
    '''
    if indexes[-1] > len(array) or len(indexes) != len(items):
        raise IndexError

    array = array[:]
    for index, item in zip(indexes, items):
        array[index] = item
    return array


def get_number_multiples(number, base=None, maximum=20):
    '''
    return all possibles multiples between 0 and the maximum given.
    '''
    number = remap_number(number, value=base) if base else number
    indexes = []
    while number <= maximum:
        indexes.append(number)
        number += base
    return indexes


def split_array(array, lenght=10):
    '''
    this common utils split an array in subarray with a lenght given.
    e.g. :
    split_array([1, 5, 65, 3, 4, 3], lenght=3)
    returns: [[1, 5, 65], [3, 4, 3]]
    '''
    arrays = []
    subarray = []
    for i, item in enumerate(array):
        subarray.append(item)
        if len(subarray) == lenght:
            arrays.append(subarray)
            subarray = []
        elif i + 1 == len(array):
            arrays.append(subarray)

    return arrays


def set_array_lenght_multiple(array, multiple=10, default=None):
    '''
    this utils ensure that an array lenght is a multiple of a number given.
    When it's not the case, it append the default value, until the array
    lenght is a multiple of the multiple given.
    e.g.
    array = [5, 3, 7, 8, 5]
    set_array_lenght_multiple(array, multiple=9, default='salut')
    returns [5, 3, 7, 8, 5, 'salut', 'salut', 'salut', 'salut']
    '''
    while len(array) % multiple != 0:
        array.append(default)
    return array


def past_and_futur(array):
    '''
    this is and utils iterator who parse and array return the previous,
    current and next value.
    Usefull to comparing stuff in array
    '''
    past_element = None
    for i, element in enumerate(array):
        futur_element = array[i + 1] if i < len(array) - 1 else None
        yield past_element, element, futur_element
        past_element = element

