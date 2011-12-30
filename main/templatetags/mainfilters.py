from datetime import datetime
from datetime import timedelta 
import re

from django import template
import utils

register = template.Library()
def natural_date(value, arg):
    if not isinstance(value, datetime):
        raise Exception("Invalid data type %s given as arg." % type(value))

    comp_d = arg
    if not arg:
        comp_d = datetime.now()

    td = value - comp_d

    #if value > 0, is in future

def truncatechars(value, chars):
    return value[:chars]




def reverse_truncate_words (value, wordcount):
    is_letter = False
    wordc = 0
    value = str(value)
    for i in xrange(len(value)-1, 0, -1):
        if re.match(r"[a-zA-Z0-9_]", value[i]):
            is_letter = True
        else:
            if is_letter:
                wordc = wordc + 1
                if wordc >= wordcount:
                    return value[i:]
                is_letter = False
    return value


def truncate_words_by_maxchars(value, arg):
    return utils.truncate_words_by_maxchars(value, arg)
   



register.filter('truncate_words_by_maxchars', truncate_words_by_maxchars)
register.filter('natural_date', natural_date)
register.filter('truncatechars', truncatechars)
register.filter('reverse_truncate_words', reverse_truncate_words)
