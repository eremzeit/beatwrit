from django.utils import simplejson as json
from datetime import datetime, timedelta
import re
import pdb
import math

from django.http import HttpRequest

from main.models import *
from utils import logpath
from main.fetching import *

class WritViewPageContext():
    def __init__(self, request, writ):
        self.writ = writ
        self.bwu = None
        if request.user.is_authenticated():
            self.bwu = request.user.beatwrituser
        self.request = request
        self._user_order = None
        self._participant_set = None
        self._participant_users = None

    def get_user_order(self):
        if self._user_order:
            return self._user_order
        self._user_order = self.writ.get_user_order()
        return self._user_order

    def get_participant_set(self):
        if self._participant_set:
            return self._participant_set
        self._participant_set = self.writ.participant_set.all()
        for part in self._participant_set:
            part.can_add_to_circle_ = self.bwu.can_add_to_circle(part).issuccess()
        return self._participant_set
    
    def get_participant_users(self):
        if self._participant_users:
            return self._participant_users
        self._participant_users = self.writ.participants.all()
        return self._participant_users

    def get_additions(self):
        adds = self.writ.addition_set.all() 
        for add in adds:
            add.can_nod_ = 1 if add.can_nod(self.bwu) else 0
        return adds

    def get_new_additions(self):
        if not self.request.user.is_anonymous():
            return []
        
        #get the additions of the user in reverse order
        my_adds = self.writ.addition_set.filter(author__exact=self.bwu).order_by('-position')
        
        if len(my_adds) is 0:
            if not self.bwu in self.writ.participants.all():
                return []
            return self.writ.addition_set.all()
        most_recent_addition = my_adds[0]
        most_recent_position = most_recent_addition.position
        return self.writ.addition_set.filter(position__gt=most_recent_position)

    def get_participant_infos(self):
        # [{'name':'', 'nodcount':''},...]
        infos = [] 
        users = self.get_user_order()
        for bwuser in users:
            p_nods = Nod.objects.filter(addition__writ__id__exact=self.writ.id,receiver__pk__exact=bwuser.id)
            info = {'name':bwuser.get_penname(), 'nodcount':len(p_nods), 'id':bwuser.pk, 'can_add':self.bwu.can_add_to_circle(bwuser).issuccess()}
            infos.append(info)
        return infos

    def get_user_json_object(self):
        user = {}
        user['nodsRemaining'] = self.get_user_nods_remaining()
        user['id'] = self.bwu.id
        user['inWrit'] = self.bwu in self.writ.participants.all()
        print user
        return json.dumps(user)

    def get_writ_json_object(self):
        writ = {}
        writ['id'] = self.writ.pk
        writ['endingType'] = self.writ.settings.endingtype
        writ['numContribWords'] = self.writ.settings.max_words_per_contribution
        writ['wordsRemaining'] = self.writ.get_words_remaining()

        adds = {}
        for addition in self.writ.addition_set.all():
            addition_info = addition.pack()
            adds[str(addition_info['id'])] = addition_info
        writ['additions'] = adds

        return json.dumps(writ)

    def is_users_turn(self):
        user_order = self.get_user_order() 
        if user_order[0].pk == self.bwu.pk: 
            return True
        else: 
            return False
    
    def is_user_participant(self):
        if self.bwu in self.get_participant_users():
            return True
        else:
            return False

    def get_user_nods_remaining(self):
        if not self.is_user_participant():
            return 0
        return self.bwu.nods_remaining

    def user_has_nods(self):
        if self.get_user_nods_remaining() > 0:
            return True
        return False

    def make_addition_html(self, addition):
        template = Template("""<span id='add_{{ addition.pk }}' add_id='{{addition.pk}}'  
           {% if addition in wvc.get_new_additions %} 
              class='add_span new_addition'   
           {% else %} 
              class='add_span'   
           {% endif %} 
           >{{addition.content}}</span> 
        """)



        """
        {% for addition in writ.addition_set.all %} 
           <span id='add_{{ addition.pk }}' add_id='{{addition.pk}}'  
           {% if addition in wvc.get_new_additions %} 
              class='add_span new_addition'   
           {% else %} 
              class='add_span'   
           {% endif %} 
           >{{addition.content}}</span> 
        {% endfor %}
        """
        
    def can_user_join(self):
        if self.writ.can_join(self.bwu).issuccess():
            return True
        else:
            return False
        
