from math import log10


BRPHONECODE = '+55'
COUNTRYCODE = '+'

def lendigits(n):
    n = abs(n)
    if n > 0:
        digits = int(log10(n))+1
        return digits
    return 1


def phone_canonicalform(number):
    if number.startswith(COUNTRYCODE):
        canonicalForm = COUNTRYCODE + ''.join([c for c in number if c.isdigit()])
        return canonicalForm
    raise ValueError('Missing country code and possibly region code')
