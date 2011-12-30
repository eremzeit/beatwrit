#!/usr/bin/python
# vim: set fileencoding=utf-8 :

#import json
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
from utils import rand_sentence, contribution_generator

names = [('Samuel,L\xc3\xa9a', 'Wright'), ('Emma', 'Johnsen'), ('Jack', 'Jackson'), ('Liam', 'Mendoza'), ('Ramos', 'Castillo'), ('Juan', 'Davis'), ('Navarro', 'Davis'), ('Daniel', 'Berg'), ('David', 'Hansen'), ('Daniel', 'Russo'), ('Nicholas', 'Olsen'), ('Aiden', 'Jackson'), ('Noah', 'Pascual'), ('Daniel', 'Ramos'), ('Ava', 'Castillo'), ('Chloe', 'Marino'), ('Brooklyn', 'Larsen'), ('Liam', 'Conti'), ('Emma', 'Karlsen'), ('Cayden', 'Johnson'), ('Florence', 'White'), ('Madison', 'Pettersen'), ('Rosalie', 'Esposito'), ('Maika', 'Johansen'), ('Camille', 'Robinson'), ('Alexander', 'Johnson'), ('Gabrielle', 'Esposito'), ('Jayden', 'Bianchi'), ('Olivia', 'Bianchi'), ('Matthew', 'Kristiansen'), ('Jack', 'Olsen'), ('Joseph', 'Pettersen'), ('Hailey', 'Larsen'), ('Hailey', 'Thompson'), ('Emma', 'Gallo'), ('Hailey', 'Navarro'), ('Madison', 'Castillo'), ('Brooklyn', 'Conti'), ('Bobby', 'Johnson'), ('Maika', 'Navarro'), ('Hannah', 'Hansen'), ('Michael', 'Green'), ('Liam', 'Jensen'), ('Mia', 'Robinson'), ('Brooklyn', 'Wright'), ('Joseph', 'Clarke'), ('Mia', 'Villanueva'), ('Brooklyn', 'Villanueva'), ('Jacob', 'Marino'), ('David', 'Conti'), ('Jayden', 'Mendoza'), ('Joseph', 'Wilson'), ('Logan', 'Mendoza'), ('Jack', 'Russo'), ('Emma', 'Larsen'), ('Emily', 'Marino'), ('Chloe', 'Brown'), ('Mia', 'Nilsen'), ('Samuel,L\xc3\xa9a', 'Johnsen'), ('Maika', 'Johnsen'), ('Emma', 'Bianchi'), ('Ramos', 'Jones'), ('Noah', 'Navarro'), ('Jayden', 'Roberts'), ('Rosalie', 'Mercado'), ('Madison', 'Esposito'), ('Lucas', 'Wilson'), ('Brooklyn', 'Larsen'), ('Jack', 'Johnson'), ('Bobby', 'Olsen'), ('Liam', 'Pettersen'), ('Juan', 'Johansen'), ('Jack', 'Clarke'), ('Navarro', 'Hall'), ('Olivia', 'Williams'), ('Jacob', 'Taylor'), ('Joseph', 'Karlsen'), ('Alexander', 'Andersen'), ('Maika', 'Ricci'), ('David', 'Taylor'), ('Jacob', 'Villanueva'), ('Samuel,L\xc3\xa9a', 'Berg'), ('Alexander', 'Walker'), ('Rosalie', 'Jones'), ('Jacob', 'Green'), ('Olivia', 'Marino'), ('Nicholas', 'Rivera'), ('Olivia', 'Pedersen'), ('Noah', 'Brown'), ('Juliette', 'Russo'), ('Logan', 'Rivera'), ('Brooklyn', 'Robinson'), ('Olivia', 'Kristiansen'), ('Hailey', 'Larsen'), ('Emma', 'Mercado'), ('Hannah', 'Bruno'), ('Logan', 'Colombo'), ('Ava', 'Pettersen'),
        ('Jacob', 'Castillo'), ('Jacob', 'Castillo'), ('Mercado', 'Aquino'), ('Emma', 'Castillo'), ('Brooklyn', 'Marino'), ('Emily', 'Gallo'), ('Jacob', 'Clarke'), ('Maika', 'Pascual'), ('Samuel,L\xc3\xa9a', 'Jones'), ('Jade', 'Ramos'), ('Olivia', 'Ramos'), ('Daniel', 'Kristiansen'), ('Samuel,L\xc3\xa9a', 'Jones'), ('Diago', 'Williams'), ('Bobby', 'Williams'), ('Florence', 'Villanueva'), ('Lucas', 'Walker'), ('Mercado', 'Thompson'), ('Ava', 'Russo'), ('Navarro', 'Ricci'), ('Madison', 'Taylor'), ('Aiden', 'White'), ('Alexander', 'White'), ('Joseph', 'Ferrari'),
        ('Jacob', 'Pascual'), ('Brooklyn', 'Clarke'), ('Hailey', 'Roberts'), ('Alexis', 'Bruno'), ('Daniel', 'Larsen'), ('Liam', 'Andersen'), ('Maika', 'Jones'), ('Nicholas', 'Aquino'), ('Jayden', 'Evans'), 
        ('Joseph', 'Bianch'), ('Mia', 'Wilson'), ('Emma', 'Olsen'), ('Jack', 'Esposito'), ('Nicholas', 'Conti'), ('Joseph', 'Mendoza'), ('Diago', 'White'), ('Camille', 'Johansen'), ('Mia', 'Robinson'), ('Hannah', 'Hall'), ('Jacob', 'Hansen'), ('Rosalie', 'Mercado'), ('Navarro', 'Walker'), ('Michael', 'Pedersen'), ('Samuel,L\xc3\xa9a', 'Bruno'), ('Rosalie', 'Hall'), ('Olivia', 'Johnson'), ('Bobby', 'Romano'), ('Jayden', 'Davis'), ('Jack', 'Jensen'), ('Alexis', 'Andersen'), ('Ramos', 'Bianchi'), ('Emily', 'Wright'), ('Bobby', 'Johnson'), ('Gabrielle', 'Clarke'), ('Maika', 'Ricci'), ('Jack', 'Pedersen'), ('Nicholas', 'Nilsen'), ('Rosalie', 'Smith'), ('Florence', 'Ricci'), ('Nicholas', 'Jackson'), ('Jack', 'Roberts'), ('Alexis', 'Pedersen'), ('Joseph', 'Aquino'), ('Alexander', 'Bruno'), ('Emma', 'Brown'), ('Brooklyn', 'Hansen'), ('Jacob', 'Hansen'), ('Maika', 'Brown'), ('Daniel', 'Navarro'), ('Rosalie', 'Pettersen'), ('Jayden', 'Rivera'), ('Camille', 'Larsen'), ('Rosalie', 'Bianchi'), ('Ava', 'Aquino'), ('Florence', 'Green'), ('Mercado', 'Bianchi'), ('Joseph', 'Pettersen'), ('Jade', 'Ramos'), ('Emma', 'Esposito'), ('Hannah', 'Rivera'), ('Mia', 'Mendoza'), ('Florence', 'Wilson'), ('Emily', 'Andersen'), ('Samuel,L\xc3\xa9a', 'Smith'), ('Diago', 'Karlsen'), ('Hailey', 'Williams'), ('Jade', 'Jensen'), ('Jack', 'Johnsen'), ('Lucas', 'Taylor'), ('Emma', 'Wilson'), ('Juliette', 'Bianchi'), ('Joseph', 'Taylor'), ('Bobby', 'Mercado'), ('Maika', 'Olsen'), ('Navarro', 'Robinson'), ('Ramos', 'Rivera'), ('Juliette', 'Jensen'), ('Camille', 'Bruno')]

defined_users = [('Peter','Venkman'), ('Louis','Tully'), ('Walter','Peck'), ('Alice','Drummand'), ('Kevin','Windermire'), ('Urma','Dorvinmire'), ('Jack','Emo'),]



def rand_first():
    return firstnames[randint(0, len(firstnames)-1)]
   
def rand_last():
    return lastnames[randint(0, len(lastnames)-1)]
    
     
def get_random_user():
    c = BeatwritUser.objects.count()
    if c:
        return BeatwritUser.objects.all()[randint(0,c-1)]
    else:
        return None

def rand_date():
    m = randint(1,12)
    d = randint(1,30)
    if m is 2 and d > 28:
        d = 28
    return datetime(randint(2008,2010), m, d)



def make_writ(user_list=None, random_settings=True):
    if not user_list:
        i = 0
        user_list = []
        while i < randint(2,20):
            user = get_random_user()
            if not user in user_list:
                user_list.append(user)
                i = i + 1

    from main.email import EmailManager
    EmailManager.is_sending_enabled = False
   
     
    start_date = rand_date()
    w = Writ()
    if random_settings: 
        ws = WritSettingsFactory.random(current_date=start_date) 
    else:
        ws = WritSettingsFactory.default(current_date=start_date) 
    
    cont_gen = contribution_generator(ws.max_words_per_contribution)
    w.init(user_list[0], ws, cont_gen.next(), save=False)
    w.is_testing = True
    w.startdate = start_date
    
    w.update_state() 
    w.save()

    for i in xrange(1, len(user_list)):
        w.add_participant(user_list[i], force=True)
    w.save()
        
    #Participants take turns creating additions
    additions = []
    users = w.get_user_order()
    for i in xrange(1, 2*len(users)-1):
        author = w.get_user_order()[0]
        content = cont_gen.next() 
        add = w.add_addition(author, content, force=True)
        additions.append(add)
    
        #if all users have written at least once
        if i >= len(users) and randint(0,100) > 20:
            r = random.randint(1,len(users))
            rand_add = additions[randint(0, len(additions)-1)]
            
            #this code isn't using the proper interface to create nods
            try:
                n = Nod()
                n.giver = author
                n.receiver = rand_add.author
                n.addition = rand_add
                n.writ = w
                n.save()
                w.total_nod_count = w.total_nod_count + 1
            except Exception, e:
                print e
                
    EmailManager.is_sending_enabled = True

def make_superuser():
    user = django.contrib.auth.models.User.objects.create_user('erem', 'erem.gumas@gmail.com','erem') 
    user.first_name = 'erem'
    user.last_name = 'gumas'
    user.is_superuser = True
    user.is_staff = True
    user.save()

    bwu = BeatwritUser()
    bwu.facebookid = randint(0,1337)
    bwu.authuser = user
    bwu.save()
    return bwu

def make_users(names_list):
    u = []
    for name in names_list:
        first = name[0]
        last = name[1] 
        
        uname = first.lower() + '_' + last.lower() + str(randint(0,1000))
            
        user = django.contrib.auth.models.User.objects.create_user(uname, uname + '@example.com', uname)
        user.joindate = rand_date()
        user.first_name = first
        user.last_name = last
        user.save()
        
        bwu = BeatwritUser()
        bwu.facebookid = randint(0, 1000000)
        bwu.authuser = user
        bwu.save()
        
        #this patch of code is causing odd problems with mysql
        user_count = BeatwritUser.objects.count()
        for i in xrange(0, min(1, user_count / 2)):
            ru = get_random_user()
            if not ru in bwu.circle.all():
                bwu.circle.add(ru)
        
        #bwu.save()
        u.append(bwu)
    return u

def make_test_data():
    random.seed(0)
    
    #first writ
    u = make_users(defined_users[:20])
    su = make_superuser()
    u = [su] + u
    make_writ(u, random_settings=False)
    
    #other writs
    names_count = 20
    writs_count = 50
    u = make_users(names[:names_count])
    for i in xrange(0,writs_count):
        make_writ(user_list=None)
    
    print 'Writs count %s' % Writ.objects.all().count()
    print 'Additions count %s' % Addition.objects.all().count()
    print 'BeatwritUsers count %s' % BeatwritUser.objects.all().count()


class WritSettingsFactory():
    @classmethod
    def default(cls, current_date=None):
        ws = WritSettings()
        #if not current_date:
        #    current_date = datetime.now()
        #dt = timedelta(days=30)
        #ws.endingdate = current_date + dt
        ws.save()
        return ws
    
    @classmethod
    def random(cls, current_date=None):
        """who_can_join = enum('FULL_PUBLIC', 'INVITE_ONLY', 'FRIENDS_ONLY')
        ending_type = enum('WORD_LIMIT', 'TIME_LIMIT', 'INACTIVITY', 'INACTIVE_ROUND')
        turn_type = enum('FREE_FOR_ALL', 'ROUND_ROBIN')
        public_visibility = enum('FRIENDS','ONLY_AUTHORS', 'FULL_PUBLIC')"""
        
        ws = WritSettings()
        ws.save()
        
        #max_words_per_contribution
        r = random_pick(list(WritSettings.CONTRIB_SIZE_CHOICES) + [(random.randint(10,500),  'custom')])
        ws.max_words_per_contribution = r[0]
        
        #is_publically_browsable = models.BooleanField(help_text=ht, default=False)
        r = random_pick(list(WritSettings.PUBLIC_VISIBILITY_CHOICES) + 2*[(WritSettings.choices.public_visibility.FULL_PUBLIC,)])
        ws.public_visibility = r[0]

        if (ws.public_visibility != WritSettings.choices.public_visibility.FULL_PUBLIC):
            ws.who_can_join = WritSettings.choices.who_can_join.FULL_PUBLIC
        else:
            r = random_pick(list(WritSettings.WHO_CAN_JOIN_CHOICES))
            ws.who_can_join = r[0]

        #endingtype = models.CharField(help_text=ht, default='time-limit',max_length=10)
        r = random_pick(list(WritSettings.ENDING_TYPE_CHOICES))
        ws.endingtype = r[0]

        #This should be null unless ending type is wordlimit
        #wordlimit = models.PositiveSmallIntegerField(help_text=ht, default=False)
        if ws.endingtype == WritSettingsChoices.ending_type.WORD_LIMIT:
            ws.wordlimit = random.randint(20, 2000)

        #inactive_time = models.PositiveIntegerField(help_text=ht, null=True)
        elif ws.endingtype == WritSettingsChoices.ending_type.INACTIVITY or ws.endingtype == WritSettingsChoices.ending_type.INACTIVE_ROUND:
            ws.inactive_time = random.randint(86400, 1000000)
        
        #endingdate = models.DateTimeField(help_text='Is null if endingtype is not time-limit')
        elif ws.endingtype == WritSettingsChoices.ending_type.TIME_LIMIT:
            if not current_date:
                current_date = datetime.now()
            dt = timedelta(days=random.randint(2, 30))
            ws.endingdate = current_date + dt
            if not ws.endingdate:
                pdb.set_trace()
        else:
            raise Exception ("aoue")
            

        #turntype = models.CharField(help_text=ht, default='round-robin', max_length=20)
        r = random_pick(list(WritSettings.TURN_TYPE_CHOICES))
        ws.turntype = r[0]

        #turn_length = models.PositiveIntegerField(help_text=ht, default=1440)
        if ws.turntype != WritSettingsChoices.turn_type.FREE_FOR_ALL:
            r = random_pick(list(WritSettings.TURN_LENGTH_CHOICES) + [(random.randint(30, 10000), 'custom')])
            ws.turn_length = r[0]

        ws.extra = 'created by: WritSettingsFactory.random()'
        ws.save()
        return ws

def random_pick(_list):
    n = random.randint(0,len(_list)-1)
    return _list[n]


if __name__ == "__main__":
    make_test_data()
