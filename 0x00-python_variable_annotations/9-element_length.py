#!/usr/bin/env python3
"""Complex types - list of floats"""
from typing import List, Tuple, Sequence


def element_length(lst: List[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns list of tuples, each containing a sequence and its length"""
    return [(i, len(i)) for i in lst]
