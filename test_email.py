
from django.utils import simplejson as json
from datetime import datetime
from datetime import timedelta 
from random import randint
import random
import pdb
import re
import os
import sys
sys.path.append ('/home/erem/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'beatwrit.settings'
from main.models import *
import django.contrib.auth.models
import beatwrit.settings

from django.core.mail import send_mail

print 'Sending....'
send_mail('Subject here', 'Here is the message.', 'account@beatwrit.com',
    ['erem.gumas@gmail.com'], fail_silently=False)
print 'DONE!'
