from datetime import datetime, timedelta
import re
import pdb
import math

from django.http import HttpRequest
from django.utils import simplejson as json


from main.models import *
from main.fetching import *
from utils import logpath, ParameterCleaner

from main.pagecontexts.writview import *
from main.pagecontexts.mybeatwrits import *

class BrowseWritsTable():
    browse_page_url = '/browse'
    legal_params = {
                    'sort':(r'recent|nods|views', 'recent'), 
                    'time': (r'today|week|all','all'),
                    'csize': (r'all|singleword|phrase|sentence|shortsentence|paragraph|unlimited','all'),
                    'onlyfinished': (r'0|1','0'),
                    'page': (r'\d+','0'),
                    'pagesize':(r'\d+','10'),
                    'joinable': (r'0|1','0'),
                    }
    
    def __init__(self, params, bwuser=None):
        self.bwuser = bwuser
        self.param_dict = ParameterCleaner.clean(self.legal_params,params)
        self._perform_query()
        self._create_page_links()
        
    def _perform_query(self):
        p = self.param_dict
        if p['sort'] == 'recent':
            writs = Writ.objects.order_by('-last_addition_date')
        elif p['sort'] == 'nods':
            writs = Writ.objects.order_by('-total_nod_count')
        elif p['sort'] == 'views':
            writs = Writ.objects.order_by('-total_view_count')

        if p['onlyfinished'] == '1':
            writs = writs.filter(endeddate__isnull=False)
        elif p['onlyfinished'] == '0':
            pass
       
        if p['time'] == 'all':
            pass
        elif p['time'] == 'today':
            yesterday = datetime.today() - timedelta(days=1)
            writs = writs.filter(last_addition_date__gt=yesterday)
        elif p['time'] == 'week':
            lastweek = datetime.today() - timedelta(days=7)
            writs = writs.filter(last_addition_date__gt=lastweek)
             
        if p['csize'] == 'all':
            pass
        elif p['csize'] == 'singleword':
            writs = writs.filter(settings__max_words_per_contribution=1)
        elif p['csize'] == 'phrase':
            writs = writs.filter(settings__max_words_per_contribution__gt=1, settings__max_words_per_contribution__lte=5)
        elif p['csize'] == 'shortsentence':
            writs = writs.filter(settings__max_words_per_contribution__gte=6, settings__max_words_per_contribution__lte=15)
        elif p['csize'] == 'sentence':
            writs = writs.filter(settings__max_words_per_contribution__gte=16, settings__max_words_per_contribution__lte=25)
        elif p['csize'] == 'paragraph':
            writs = writs.filter(settings__max_words_per_contribution__gte=26)
        elif p['csize'] == 'unlimited':
            writs = writs.filter(settings__max_words_per_contribution=0)
        
        #limit to public writs
        writs = writs.filter(settings__public_visibility=WritSettingsChoices.public_visibility.FULL_PUBLIC)
       
        #limit to joinable writs
        if p['joinable'] == '1':
            if (self.bwuser):
                #this won't change
                writs = writs.filter(settings__who_can_join=WritSettings.choices.who_can_join.FULL_PUBLIC)
            else:
                writs = writs.filter(settings__who_can_join=WritSettings.choices.who_can_join.FULL_PUBLIC)

        r0 = 0
        r1 = 0
        try:
            page = int(p['page'])
            pagesize = min(int(p['pagesize']), 50)
            r0 = page * pagesize
            r1 = r0 + pagesize
        except:
            pass

        writ_count = writs.count()
        print 'Query returned %s total writs' % writ_count
        self.page_count = int(math.ceil(float(writ_count) / float(pagesize)))

        self.writs = writs[r0:r1]

    def _recreate_url_params(self):
        pstring = '?'
        for key, item in self.param_dict.items():
            if not key == 'page':
                if not item == self.legal_params[key][1]:
                    pstring = pstring + '%s=%s&' % (key, item)
        
        if pstring:
            if pstring[-1] == '&':
                pstring = pstring[:-1]
        return pstring
    
    def _create_page_links(self):
        pagelinks = []
        pstring = self._recreate_url_params()
        for i in xrange(self.page_count):
            url = self.browse_page_url + pstring + '&page=' + str(i)
            pagelinks.append("<a href='%s'>%s</a>" % (url, i+1))
        self.pagelinks = pagelinks
    
    def get_writs(self):
        return self.writs

    def get_page_links(self):
        return self.pagelinks
    
    def get_params(self):
        return self.param_dict
    def get_browse_url(self):
        return self.browse_page_url

class LandingPageContext():
    def __init__(self, request):
        self.writs_most_nods = []
    def get_writs_most_nods(self, count=4):
        if not len(self.writs_most_nods) >= count:
            self.writs_most_nods = WritsSurface.coolest()
        return self.writs_most_nods
