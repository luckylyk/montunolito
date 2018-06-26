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