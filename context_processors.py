#import json
from django.utils import simplejson as json
import datetime
import pdb

from django.http import HttpRequest
from django.db import connection
from django.template import Template, Context

from main.models import *
from utils import logpath
from conditions import ConditionList

def log(HttpRequest):
    f = open(logpath, 'r')
    s = str(f.read())
    print 'Log: ' + s
    return {'log': 'Log:' + s}

def sqlinfo(HttpRequest):
    time = 0.0
    for q in connection.queries:
        time += float(q['time'])

    t = Template('''
        <p><em>Total query count:</em> {{ count }}<br/>
        <em>Total execution time:</em> {{ time }}</p>
        <ul class="sqllog">
            {% for sql in sqllog %}
                <li>{{ sql.time }}: {{ sql.sql }}</li>
            {% endfor %}
        </ul>

    ''')

    s = t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))
    return {'sqlinfo':s} 


def automessage (HttpRequest):
    d = {}
    h = HttpRequest
    if h.GET:
        print h.GET
        if 'msg' in h.GET:
            val = -1
            try:
                val = int(h.GET['msg'])
                if ConditionList[val].issuccess():
                    d['msg'] = ConditionList[val].message
                else:
                    d['error'] = ConditionList[val].message
                print 'automessage dict: %s' % d
                return d
            except:
                pass
    return {}
