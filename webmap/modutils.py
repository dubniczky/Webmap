'''
Short utility functions for modifying data
'''

def trimf(f: float, decimal_points: int = 2) -> str:
    '''Trims the float to two decimal points by default and returns the string.'''
    return str( round(f, decimal_points) )

def unique_list(l: list) -> list:
    '''Removes duplicates from a list without preserving order'''
    return list(set(l))
