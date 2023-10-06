#!/usr/bin/env python3
"""Augment the following code with the correct duck-typed annotations:

# The types of the elements of the input are not know
def safe_first_element(lst):
    if lst:
        return lst[0]
    else:
        return None

{'lst': typing.Sequence[typing.Any], 'return': \
    typing.Union[typing.Any, NoneType]}
"""
from typing import Any, List, Union


def safe_first_element(lst: List[Union[Any, None]]) -> Union[Any, None]:
    """
    Safely retrieves the first element of a list, or returns
    None if the list is empty.
    :param lst: A list that can contain elements of any type or None.
    :return: The first element of the list or None if the list is empty.
    """
    if lst:
        return lst[0]
    else:
        return None
