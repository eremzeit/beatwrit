from django.utils import simplejson as json
from datetime import datetime, timedelta
import re
import pdb
import math

from django.http import HttpRequest

from main.models import *
from utils import logpath
from main.fetching import *
from main.html import WritListWidgetHTML

class MyBeatwritPageContext():
    def __init__(self,bwuser):
        self.active_writs = None
        self.historic_writs = None
        self.friends_writs = None
        self.community_writs = None
        self.my_recent_addition_locales = None
        self.community_recent_addition_locales = None
       
        self.bwuser = bwuser
        #self.my_recent_addition_locales = self.get_user_recent_addition_locales()
        #self.community_recent_addition_locales = self.get_community_recent_addition_locales()

    def get_bwuser(self):
        return self.bwuser
    
    def get_active_writs(self):
        if not self.active_writs:
            accessor = WritsAccessor(self.bwuser)
            self.active_writs = accessor.users_active_by_date(self.bwuser, pagenum=0, pagesize=10, force=True)
        return self.active_writs
    
    def get_finished_writs(self):
        if not self.historic_writs:
            accessor = WritsAccessor(self.bwuser)
            self.historic_writs = accessor.users_completed_by_date(self.bwuser, pagenum=0, pagesize=10, force=True)
        return self.historic_writs
    
    def get_circle_writs(self):
        if not self.friends_writs:
            accessor = WritsAccessor(self.bwuser)
            self.friends_writs = accessor.users_circle_by_date(self.bwuser, pagenum=0, pagesize=10, force=True)
        return self.friends_writs
    
    def get_community_writs(self):
        if not self.community_writs:
            self.community_writs = WritsSurface.coolest(limit=10)
        return WritListWidgetHTML.community_writs(self.community_writs)
    
    def active_writs_html(self):
        return WritListWidgetHTML.active_writs(self.get_active_writs())
    
    def finished_writs_html(self):
        return WritListWidgetHTML.finished_writs(self.get_finished_writs())
    
    def circle_writs_html(self):
        return WritListWidgetHTML.circle_writs(self.get_circle_writs())
    
    def community_writs_html(self):
        return WritListWidgetHTML.community_writs(self.get_community_writs())

    def is_turn_in_any(self):
        active_writs = self.get_active_writs()
        writs_of_turn = []
        for writ in active_writs:
            if writ.settings.turntype == WritSettingsChoices.turn_type.ROUND_ROBIN  and writ.is_users_turn(self.bwuser):
                writs_of_turn.append(writ)
                return True
        return False 
   
    def get_user_recent_addition_locales(self, count=10):
        if self.my_recent_addition_locales == None:
            self.my_recent_addition_locales = []
        if not len(self.my_recent_addition_locales) >= count:
            self.my_recent_addition_locales = self._get_recent_addition_locales(self.bwuser.addition_set.all()[:count] ,count=count)
        return self.my_recent_addition_locales
    
    def get_community_recent_addition_locales(self, count=10):
        if self.community_recent_addition_locales == None:
            self.community_recent_addition_locales = []
        if not len(self.community_recent_addition_locales) >= count:
            self.community_recent_addition_locales = self._get_recent_addition_locales(AdditionsSurface.coolest()[:count], count=count)
        return self.community_recent_addition_locales
            
    
    #Pass a queryset of Additions
    #Returns a list of count AdditionLocals
    def _get_recent_addition_locales(self, additions, count=10):
        locale_list = []
        for addition in additions:
            #get the additions immediately before and after the current addition (should yield at most 3 additions and at least 1)
            sampled_additions = addition.writ.addition_set.filter(position__gte=addition.position-1, position__lte=addition.position+1).order_by('position').all()
           
            locale = None 
            #Organize context into tuple
            if len(sampled_additions) == 3:
                locale = AdditionLocale(tuple(sampled_additions))
            elif len(sampled_additions) == 2:
                if sampled_additions[0].id == addition.id:
                    locale = AdditionLocale(None, addition, sampled_additions[1])
                if sampled_additions[1].id == addition.id:
                    locale = AdditionLocale(sampled_additions[0], addition, None)
            elif len(sampled_additions) == 1:
                locale = AdditionLocale(None, addition, None)
            locale_list.append(locale)
        return locale_list

    def get_user_recent_addition_locales_json(self, count=10):
        locale_list = self.get_user_recent_addition_locales(count=count)
        r = []
        for locale in locale_list:
            if locale:
                r.append(locale.pack())
            else:
                r.append(None)
        return json.dumps(r)
    
    def get_community_recent_addition_locales_json(self, count=10):
        locale_list = self.get_community_recent_addition_locales(count=count)
        r = [] 
        for locale in locale_list:
            if locale:
                r.append(locale.pack())
            else:
                r.append(None)
        return json.dumps(r)

class AdditionLocale():
    before = None;
    current = None;
    after = None;
    
    def __init__(self, *args):
        if len(args) == 1 and len(args[0]) == 3:
            self.before = args[0][0]
            self.current = args[0][1]
            self.after = args[0][2]
        elif len(args) == 3:
            self.before = args[0]
            self.current = args[1]
            self.after = args[2]
    
    def __getitem__(self,key):
        key = int(key)
        if key == 0:
            return self.before
        elif key == 1:
            return self.current 
        elif key == 2:
            return self.after 
        else:
            raise Exception("Invalid index requested: %s" % key)
    def pack(self):
        r = []
        if self.before:
            r.append(self.before.pack())
        else:
            r.append(None)
        
        if self.current:
            r.append(self.current.pack())
        else:
            r.append(None)
        
        if self.after:
            r.append(self.after.pack())
        else:
            r.append(None)
        return r 
