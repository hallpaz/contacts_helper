from math import log10


BRPHONECODE = '55'
RJPHONECODE = '21'
PLUS = '+'
RJLENPHONE = 9
RJSTARTPHONE = '9'

def lendigits(n):
    n = abs(n)
    if n > 0:
        digits = int(log10(n))+1
        return digits
    return 1


def phone_canonicalform(number):
    # TODO: deal with the case where there is no country code
    allnumbers = ''.join([c for c in number if c.isdigit()])
    canonicalForm = ""
    if number.startswith(PLUS):
        canonicalForm = PLUS + allnumbers
    elif len(allnumbers) == RJLENPHONE and allnumbers[0] == RJSTARTPHONE:
        canonicalForm = PLUS + BRPHONECODE + RJPHONECODE + allnumbers
    elif allnumbers[0] == '0' and len(allnumbers) >= 11:
        canonicalForm = PLUS + BRPHONECODE + allnumbers[1:]
    elif allnumbers[0] != '0' and len(allnumbers) >=10:
        canonicalForm = PLUS + BRPHONECODE + allnumbers
    else:
        print("Número irregular: ", number, "REP: ", allnumbers)
        canonicalForm = number
    # raise ValueError('Missing country code and possibly region code')
    return canonicalForm
