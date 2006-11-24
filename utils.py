"""Utility functions and classes for PyFeyn"""


def sign(x):
    """Get the sign of a numeric type"""
    if x < 0: return -1
    if x > 0: return 1
    if x == 0: return 0


class Visible:
    def isVisible():
        return True
