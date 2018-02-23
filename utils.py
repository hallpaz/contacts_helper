from math import log10


def lendigits(n):
    n = abs(n)
    if n > 0:
        digits = int(log10(n))+1
    return 1
