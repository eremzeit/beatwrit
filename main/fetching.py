import random

from main.models import *
from main.access import AccessModel
from datetime import datetime, timedelta
from utils import PermissionsException

import django.contrib.auth.models
import pdb

fullpublic = WritSettingsChoices.public_visibility.FULL_PUBLIC


#should you first instantiate this class and pass the context before calling a member function?
class WritsAccessor():
    def __init__(self, bwuser):
        if isinstance(bwuser, django.contrib.auth.models.User) and bwuser.isanonymous():
            self.context_bwuser = None
        else:
            self.context_bwuser = bwuser
    
    def users_active_by_date(self, bwuser, pagenum=0, pagesize=10, force=False):
        if not force and not AccessModel.can_access_profile(self.context_bwuser, bwuser):
            raise ProfilePermissionsException()
        p = pagenum * pagesize
        q = p + pagesize
        return bwuser.writ_set.filter(is_active=True).order_by('-last_addition_date')[p:q]

        """def get_recent_writs(self, count=-1, onlyactive=False):
            #writids = Participant.objects.filter(beatwrituser__pk__exact=self.pk).values_list('writ', flat=True)
            if onlyactive:
                writs = self.writ_set.filter(endeddate__isnull=True).order_by('-last_addition_date')
                #writs = Writ.objects.filter(participants__id=self.pk, endeddate__isnull=False).order_by('-last_addition_date')
            else:
                writs = self.writ_set.order_by('-last_addition_date')
                #writs = Writ.objects.filter(participants__id=self.pk).order_by('-last_addition_date')
            if count >= 0:
                return writs[:count]
            else:
                return writs[:]"""


    def users_completed_by_date(self, bwuser, pagenum=0, pagesize=10, force=False):
        if not force and not AccessModel.can_access_profile(self.context_bwuser, bwuser):
            raise ProfilePermissionsException()
        p = pagenum * pagesize
        q = p + pagesize
        return bwuser.writ_set.filter(is_active=False).order_by('last_addition_date')[p:q]
   
    def users_circle_by_date(self, bwuser, pagenum=0, pagesize=10, force=False):
        if not force and not AccessModel.can_access_profile(self.context_bwuser, bwuser):
            raise ProfilePermissionsException()
        p = pagenum * pagesize
        q = p + pagesize
        #return Writ.objects.filter(participants__in=bwu.circle.all()).order_by('last_addition_date')[p:q]
        return Writ.objects.filter(participants__circle__id=bwuser.circle.all()).order_by('last_addition_date')[p:q]
    
    @staticmethod
    def community_by_date(bwuser, pagenum=0, pagesize=10):
        p = pagenum * pagesize
        q = p + pagesize
        return WritsSurface.public_writs_query().order_by('total_nod_count')[p:q]
        #month_ago = datetime.today() - timedelta(days=30)
        #return WritsSurface.public_writs_query().filter(last_update_date__gte=month_ago).order_by('total_nod_count')[p:q]

class AdditionsAccessor():
    pass

""" The functions in this module are temporary solutions.
    Need some dedicated tables eventually """
class WritsSurface():
    @staticmethod
    def public_writs_query():
        return Writ.objects.filter(settings__public_visibility__exact=fullpublic)
    
    @classmethod
    def most_views_today(cls, limit=100):
        return WritsSurface.public_writs_query().filter(last_update_date__gte=datetime.today()).limit.order_by('total_view_count')[:limit]

    @classmethod
    def most_views_week(cls, limit=100):
        one_week_ago = datetime.today() - timedelta(days=7)
        return WritsSurface.public_writs_query().filter(last_update_date__gte=one_week_ago).order_by('total_view_count')[:limit]
        
    @classmethod
    def most_views_month(cls, limit=100):
        month_ago = datetime.today() - timedelta(days=30)
        return WritsSurface.public_writs_query().filter(last_update_date__gte=month_ago).order_by('total_view_count')[:limit]

    @classmethod
    def most_views_all(cls, limit=100):
        return WritsSurface.public_writs_query().filter(last_update_date__gte=month_ago).order_by('total_view_count')[:limit]

    @classmethod
    def most_nods_today(cls, limit=100):
        return WritsSurface.public_writs_query().filter(last_update_date__gte=datetime.today()).order_by('total_nod_count')[:limit]

    @classmethod
    def most_nods_week(cls, limit=100):
        week_ago = datetime.today() - timedelta(days=7)
        return WritsSurface.public_writs_query().filter(last_update_date__gte=week_ago).order_by('total_nod_count')[:limit]

    @classmethod
    def most_nods_month(cls, limit=100):
        month_ago = datetime.today() - timedelta(days=30)
        return WritsSurface.public_writs_query().filter(last_update_date__gte=month_ago).order_by('total_nod_count')[:limit]

    @classmethod
    def most_nods_all(cls, limit=100):
        return WritsSurface.public_writs_query().order_by('total_nod_count')[:limit]
   
    @classmethod
    def coolest(cls, limit=20):
        grp = cls.most_nods_week(limit=limit*3)
        if (len(grp) < limit):
            grp = cls.most_nods_month(limit=limit*3)
        if (len(grp) < limit):
            grp = cls.most_nods_all(limit=limit*3)
        return random_subset(grp, limit)


class AdditionsSurface():
    fullpublic = WritSettingsChoices.public_visibility.FULL_PUBLIC
    @classmethod
    def most_nods_today(cls, limit=100):
        r = Addition.objects.filter(date__gte=datetime.today())
        r = r.filter(writ__settings__public_visibility__exact=cls.fullpublic, author__additions_surfacable__exact=True)
        r = r.order_by('total_nod_count')[:limit]
        return r

    @classmethod
    def most_nods_week(cls, limit=100):
        week_ago = datetime.today() - timedelta(days=7)
        r = Addition.objects.filter(date__gte=week_ago)
        r = r.filter(writ__settings__public_visibility__exact=cls.fullpublic, author__additions_surfacable__exact=True)
        r = r.order_by('total_nod_count')[:limit]
        return r

    @classmethod
    def most_nods_month(cls, limit=100):
        month_ago = datetime.today() - timedelta(days=30)
        r = Addition.objects.filter(date__gte=month_ago)
        r = r.filter(writ__settings__public_visibility__exact=cls.fullpublic, author__additions_surfacable__exact=True)
        r = r.order_by('total_nod_count')[:limit]
        return r

    @classmethod
    def most_nods_all(cls, limit=100):
        r = Addition.objects.filter(writ__settings__public_visibility__exact=cls.fullpublic, author__additions_surfacable__exact=True)
        r = r.order_by('total_nod_count')[:limit]
        return r
    
    @classmethod
    def coolest(cls, limit=20):
        grp = cls.most_nods_week(limit=limit*3)
        if (len(grp) < limit):
            grp = cls.most_nods_month(limit=limit*3)
        return random_subset(grp, limit)

class UsersSurface():
    @classmethod
    def most_nods_all(cls, limit=100):
        return BeatWritUser.objects.filter(additions_surfacable__exact=True).order_by('total_nods_received')[:limit]
    
    @classmethod
    def coolest(cls, limit=20):
        grp = cls.most_nods_all(limit=limit*3)
        return random_subset(grp, limit)

def random_subset(_list, size):
    if len(_list) <= size:
        return _list
    i = 0
    r = [] 
    set_dict = {}
    while i < size:
        x = random.randint(0, len(_list)-1)
        if not x in set_dict:
            r.append(_list[x])
            set_dict[x] = True
            i = i + 1
    return r




"""
    Writs.get_most_views_today()
    Writs.get_most_views_week()
    Writs.get_most_views_month()
    Writs.get_most_views_all()

    Writs.get_most_nods_today()
    Writs.get_most_nods_week()
    Writs.get_most_nods_month()
    Writs.get_most_nods_all()

    Writs.get_best_today()
    Writs.get_best_week()
    Writs.get_best_month()
    Writs.get_best_all()

    Additions.get_most_nods_today()
    Additions.get_most_nods_week()
    Additions.get_most_nods_month()
    Additions.get_most_nods_all()
"""
