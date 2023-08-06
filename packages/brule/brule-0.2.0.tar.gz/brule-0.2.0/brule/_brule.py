from string import ascii_lowercase
from random import choice

from ._names import FIRST_NAMES, LAST_NAMES

VOWELS = 'aeiou'
BAD_WITH_R = 'rjwmnh'
GENDERS = ['male', 'female']


def _get_first_name(first='', gender='male'):

    if first:
        if first in FIRST_NAMES[gender]['initials'].keys():
            return choice(FIRST_NAMES[gender]['initials'][first])
        else:
            return choice(FIRST_NAMES[gender]['other'])
            
    else:
        return choice(FIRST_NAMES[gender]['all'])


def _get_last_name(last='', gender='male'):
    
    if last:
        if last[0] in VOWELS:
            return choice(LAST_NAMES['vowel_suffix'])
        elif last[0] in BAD_WITH_R:
            return last[0].upper() + choice(LAST_NAMES['no_r_suffix'])
        else:
            return last[0].upper() + choice(LAST_NAMES['suffix'])
    else:
        return choice(LAST_NAMES['vowel_suffix'])


def first_name(first='', gender=''):
    '''
    DESC:
        Return a "Brule-ized" first name.
    
    ARGS:
        `first` *            
            First name.
            ex: (first="Steve", ...)

        `gender` *
            Gender. Can be fully spelled out
            or abbreviated.
            ex: (..., gender="m")
                (..., gender="female")

        * optional arg
    '''

    first = first.lower()
    gender = gender.lower()

    # clean `first`
    if first:
        if first[0] in ascii_lowercase:
            first = first[0]
        else:
            raise ValueError(f'Invalid name: "{first}"')
        
    # clean `gender`
    if gender:
        if gender[0] in ('m', 'f'):
            gender = 'male' if gender[0] == 'm' else 'female'
        else:
            raise ValueError(f'Invalid gender: "{gender}"')
    else:
        gender = choice(GENDERS)

    return _get_first_name(first, gender)


def last_name(last='', gender=''):
    '''
    DESC:
        Return a "Brule-ized" last name.
    
    ARGS:
        `last` *            
            Last name.
            ex: (last="Brule", ...)

        `gender` *
            Gender. Can be fully spelled out
            or abbreviated.
            ex: (..., gender="m")
                (..., gender="female")

        * optional arg
    '''

    last = last.lower()
    gender = gender.lower()

    # clean `last`
    if last:
        if last[0] in ascii_lowercase:
            last = last[0]
        else:
            raise ValueError(f'Invalid name: "{last}"')

    # clean `gender`
    if gender:
        if gender[0] in ('m', 'f'):
            gender = 'male' if gender[0] == 'm' else 'female'
        else:
            raise ValueError(f'Invalid gender: "{gender}"')
    else:
        gender = choice(GENDERS)

    return _get_last_name(last, gender)


def full_name(first='', last='', gender=''):
    '''
    DESC:
        Return a "Brule-ized" full name.
    
    ARGS:
        `first` * 
            First name.
            ex: (first="Steve", ...)

        `last` *            
            Last name.
            ex: (last="Brule", ...)

        `gender` *
            Gender. Can be fully spelled out
            or abbreviated.
            ex: (..., gender="m")
                (..., gender="female")

        * optional arg
    '''

    first = first.lower()
    last = last.lower()
    gender = gender.lower()

    # clean `first`
    if first:
        if first[0] in ascii_lowercase:
            first = first[0]
        else:
            raise ValueError(f'Invalid name: "{first}"')

    # clean `last`
    if last:
        if last[0] in ascii_lowercase:
            last = last[0]
        else:
            raise ValueError(f'Invalid name: "{last}"')

    # clean `gender`
    if gender:
        if gender[0] in ('m', 'f'):
            gender = 'male' if gender[0] == 'm' else 'female'
        else:
            raise ValueError(f'Invalid gender: "{gender}"')
    else:
        gender = choice(GENDERS)

    return _get_first_name(first, gender) + ' ' + _get_last_name(last, gender)