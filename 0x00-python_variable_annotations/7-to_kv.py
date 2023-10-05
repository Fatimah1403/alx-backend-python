#!/usr/bin/env python3
""" function to_kv that takes a string k and an int OR float v
     as arguments and returns a tuple. The first
     element of the tuple is the string k
"""
from typing import List, Union, Tuple


def to_kv(k: str, v: union[int, float]) -> Tuple[str, float]:
    """returns a tuple of the string & square of v as float """
    return (k, float(v * v))
