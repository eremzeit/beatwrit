# vim: set fileencoding=utf-8 :

import re
import random
import pdb
import sys
 
from datetime import datetime
from datetime import timedelta 

logpath = 'log.txt'

import types
from lib.BeautifulSoup import *
from types import *

#reset file
f = open(logpath, 'w')
f.close()
temp_log = 'Log Start: '

error_quotes = [
("Be bold. If you're going to make an error, make a doozy, and don't be afraid to hit the ball.","Billie Jean King"),
("Be calm in arguing; for fierceness makes error a fault, and truth discourtesy.","George Herbert"),
("All men are liable to error; and most men are, in many points, by passion or interest, under temptation to it.","John Locke"),
("A subtle thought that is in error may yet give rise to fruitful inquiry that can establish truths of great value.", "Isaac Asimov"),
("One of the most dangerous forms of human error is forgetting what one is trying to achieve.","Paul Nitze"),
("Obscurity is the realm of error.","Luc de Clapier"),
("No one who lives in error is free.", "Euripides"),
]






#An example of a valid legal_params:
#    legal_params = {
#                    'sort':(r'recent|nods|views', 'recent'), 
#                    'time': (r'today|week|all','all'),
#                    'csize': (r'all|singleword|phrase|sentence|shortsentence|paragraph|unlimited','all'),
#                    'onlyfinished': (r'0|1','0'),
#                    'page': (r'\d+','0'),
#                    'pagesize':(r'\d+','10'),
#                    }
class ParameterCleaner(object):
    """ Validates the given parameter values and uses the default values where appropriate """
    @classmethod
    def clean(cls, legal_params, params):
        param_dict = {}
        for param, item  in legal_params.items():
            regex, default = item
            
            if not param in params:
                #set it to the default value given in legal_params
                param_dict[param] = autocast_string(default)
            else:
                #validate the value
                if re.match(regex, params[param]):
                    param_dict[param] = autocast_string(params[param])
                else:
                    #otherwise set it to the default value
                    param_dict[param] = default
        print 'Browse writs params: %s' % param_dict
        return param_dict 

def autocast_string(string):
    if not type(string) is StringType:
        return str(string)
    string = string.strip()
    try:
        if re.match(r'\d+', string):
            return int(string)
    except:
        pass 
    return str(string)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def enum_ex(*mappings, **named):
    tokens = map(lambda x: x[1], mappings)
    values = map(lambda x: x[0], mappings)
    enums = dict(zip(tokens, values))

    d_shorts = {}
    d_longs = {}
    d_values = {}
    
    _dict = {}
    _dict.update(enums)
    for mapping in mappings:
        d_shorts[mapping[1]] = mapping[3]
        d_longs[mapping[1]] = mapping[2]
        d_values[mapping[1]] = enums[mapping[1]]
   
    _dict.update({'value':type('EnumValues',(), d_values)})
    _dict.update({'s':type('EnumShortStrings',(), d_shorts)})
    _dict.update({'l':type('EnumLongStrings',(), d_longs)})
   
    def isvalid(self, number):
        return number in values
    isvalid= types.MethodType(isvalid, 'EnumEx')
    _dict['isvalid'] = isvalid

    r = type('EnumEx', (), _dict)
    return r

#Definitive server-side method to find word counts for text that has html included
def find_word_count(content):
    soup = BeautifulSoup(content)
    content = soup.getText()
    return len(split_words(content))

def split_words(s):
    pat = r'[^\w_]+'
    l = re.split(pat, s)
    if len(l) > 0:
        if l[-1] == '':
            del l[-1]
    return l

def log(s, exception=False):
    global temp_log
    s = str(s) + '\n'
    f = open(logpath, 'a')
    f.write(str(s))
    f.close()
    temp_log = temp_log + s
    if exception:
        raise Exception('Log: %s' % s)

def plural(count):
    if count > 1:
        return 's'
    else:
        return ''

def contribution_generator(num_words):
    f = open('./fake_text.txt', 'r')
    orig_lorumipsum = f.read()
    _lorumipsum = []
    s = ''
    for c in orig_lorumipsum:
        if c == '.':
            s = re.sub(r'\[\d{1,3}\]', '', s)
            _lorumipsum.append(s + c)
            s = ''
        else:
            s = s + c
    lorumipsum = _lorumipsum
    
    words = orig_lorumipsum.split()
    i = random.randint(0, len(words)-1)
    
    #needs to begin where a new sentence starts at least
    w = words[i]
    while w.strip()[-1] != '.':
        i+=1
        w = words[i]
    i = i + 1 if i < len(words) else 0 

    while True:
        _num_words = 0
        if num_words == 0:
            _num_words = random.randint(1,40)
        else:
            _num_words = num_words

        s = ' '.join(words[i:i+_num_words])
        minus = 0
        while len(split_words(s)) > _num_words:
            s = ' '.join(words[i:i+_num_words-minus])
            minus = minus + 1
        if s.strip() == '':
            yield 'horses'
        else:
            yield s
        i = i + num_words
        if i >= len(words):
            i = 0

def rand_sentence():
    s = ''
    while s.strip() == '':
        s = lorumipsum[random.randint(0,len(lorumipsum)-1)]
    return s

def timedelta_from_now(date, simple=True):
    return timedelta_to_natural(datetime.now() - date)

def timedelta_to_natural(timedelta, simple=True):
    return minutes_to_natural(timedelta.days * 3600 + timedelta.seconds / 60, simple)

def minutes_to_natural(minutes, simple=False):
    mins = minutes
    weeks = 0
    days = 0
    hours = 0
    if mins == 0:
        return '0 minutes'
    
    sweeks, sdays, shours, smins = '','','',''

    weeks = mins / 10080
    if weeks:
        sweeks = '%s week%s' % (weeks,plural(weeks))
    mins = mins % 10080

    days = mins / 1440 
    if days:
        sdays = '%s day%s' % (days, plural(days))
    mins = mins % 1440 
    
    hours = mins / 60
    if hours:
        shours = '%s hour%s' % (hours, plural(hours))

    mins = mins % 60
    if mins:
        smins = '%s min%s' % (mins, plural(mins))
    
    out = ''
    time_list = [sweeks, sdays, shours, smins]
    for i in xrange(0, len(time_list)):
        if time_list[i] != '':
            if simple:
                return time_list[i]
            out = out + time_list[i] + ', '
     
    if out[-2:] == ', ':
        return out[:-2]
    if not out:
        pdb.set_trace()
    return out


def week_from_now():
    return datetime.now() + timedelta(days=7)

def random_positive_long():
    return random.randint(0, 9223372036854775807)

def timedelta_to_minutes(td):
    minutes = 0
    minutes = minutes + td.days * 24 * 60
    minutes = minutes + int(td.seconds / 60.0)
    return minutes

def get_error_quote():
    return error_quotes[random.randint(0, len(error_quotes)-1)]

def to_unicode(text):
    return unicode(decode(text))

def decode(s, guess_list=['utf-8','latin1', 'ascii', 'us-ascii','iso-8859-1','iso-8859-2','windows-1250','windows-1252']):
    for encoding in guess_list:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return s.decode('ascii', 'ignore')


def serialize_date(datetime):
    return datetime.isoformat()

def truncate_words(string, max_words):
    is_letter = False
    wordc = 0
    string = str(string)
    for i in xrange(len(string)):
        if re.match(r"[a-zA-Z0-9_]", string[i]):
            is_letter = True
        else:
            if is_letter:
                wordc = wordc + 1
                if wordc >= max_words:
                    return string[:i]
                is_letter = False
    return string 

def truncate_words_by_maxchars(string, max_chars):
    last_word_break = -1
    is_letter = False
    for i in xrange(len(string)):
        if re.match(r"[a-zA-Z0-9_]", string[i]):
            is_letter = True
        else:
            if is_letter:
                last_word_break = i
        if i >= max_chars:
            break
    if last_word_break > max_chars: raise Exception("Function doesn't work")
    if last_word_break >= 0:
        return string[:last_word_break]
    else:
        return string[:i]


#############################
###   messaging helpers   ###
#############################
class BeatwritMessaging:
    from django.contrib import messages
    @staticmethod
    def popupinfo(request, message):
        messages.add_message(request, messages.INFO+1, message,extra_tags='popupinfo')
    def popupinfo(request, message):
        messages.add_message(request, messages.SUCCESS+1, message,extra_tags='popupinfo')
    def popupinfo(request, message):
        messages.add_message(request, messages.INFO+1, message,extra_tags='popupinfo')






class WritValidityException(Exception):
    def __init__(self, problem_str):
        self.problem_str = problem_str
    def __str__(self):
        return "WritValidityException: %s" % self.problem_str

class WritSettingsValidityException(Exception):
    def __init__(self, problem_str):
        self.problem_str = problem_str
    def __str__(self):
        return "WritSettingsValidityException: %s" % self.problem_str


class PermissionsException(Exception):
    def_str = "The given user does not have permissions to access this resource."
    def __init__(self, problem_str=None):
        if problem_str:
            self.problem_str = problem_str
        else:
            self.problem_str = self.def_str
    def __str__(self):
        return "WritSettingsValidityException: %s" % self.problem_str

class WritPermissionsException(PermissionsException):
    def_str = "The user does not have permissions to access this writ."

class ProfilePermissionsException(PermissionsException):
    def_str = "The given user does not have permissions to access this user profile."


