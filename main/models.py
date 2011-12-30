#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from django.db import models
import django.contrib.auth.models
from django.utils import simplejson as json
from django.template.defaultfilters import timeuntil

from datetime import datetime
from datetime import timedelta 
import sys
import types


from utils import *
import utils
from conditions import ConditionList
import traceback
from jsonmodels import BeatwritJSON

#from main.email.email import EmailManager
import main.email




class BeatwritUserChoices:
    profile_visibility = enum_ex(
                                    (0, 'FULL_PUBLIC', 'Anyone can browse the list of your writs.', 'Public'), 
                                    (1, 'ONLY_CIRCLE', 'Only users in your circle can browse your list of writs.', 'Only Circle'), 
                                    (2, 'ONLY_AUTHOR', 'Only you can browse your list of writs.', 'Private'))

class BeatwritModel(models.Model):
    def pack(self):
        return BeatwritJSON.pack(self)
    def json(self):
        return BeatwritJSON.json(self)
    class Meta:
        abstract = True
    
class BeatwritUser(BeatwritModel):
    choices = BeatwritUserChoices
    PROFILE_VISIBILITY_CHOICES = (
        (choices.profile_visibility.ONLY_CIRCLE ,'Only Circle'),
        (choices.profile_visibility.FULL_PUBLIC,'Everyone'),
        (choices.profile_visibility.ONLY_AUTHOR,'Only Author'),
    )
    
    authuser = models.OneToOneField(django.contrib.auth.models.User)
    penname = models.CharField(max_length=50)
    facebookid = models.IntegerField(blank=True, null=True, verbose_name='Facebook User ID')
    timestamp = models.DateTimeField(auto_now=True, null=True)
    circle = models.ManyToManyField('BeatwritUser', symmetrical=False)
    nods_remaining = models.IntegerField(default=0)
    
    #database denormalization
    total_nods_received = models.IntegerField(default=0, db_index=True)
    total_additions = models.IntegerField(default=0)
    addition_locales_cache = models.TextField()

    #settings
    profile_visibility = models.SmallIntegerField(help_text="Use this to restrict who can view your list of writs.  Choices: all, friends-only, none", default=choices.profile_visibility.FULL_PUBLIC)
    additions_surfacable = models.BooleanField(default=True)
    email_reminders_enabled = models.BooleanField(help_text="Should email reminders be sent?",default=True)
    email_invites_enabled = models.BooleanField(help_text="Should emails be sent when invited to a writ?",default=True)

    

    #
    #   READONLY METHODS
    #
    def __unicode__(self):
        return self.get_penname()
    def get_penname(self):
        if self.penname != '':
            return self.penname
        else:
            au = self.authuser
            return au.first_name + ' ' + au.last_name
    
    def get_count_active_writs(self):
        writids = Participant.objects.filter(beatwrituser__pk__exact=self.pk).values_list('writ', flat=True)
        writs = Writ.objects.filter(id__in=writids, endeddate__isnull=True).order_by('-last_addition_date')
        return writs.count()
                
    def get_recent_writs(self, count=-1, onlyactive=False):
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
            return writs[:]
    def get_historic_writs(self, count=-1):
        #return Writ.objects.filter(participant__id=self.pk, endeddate__isnull=False)
        return self.writ_set.filter(endeddate__isnull=False).order_by('-last_addition_date')

    def get_circles_recent_writs(self, count=5):
        writs = Participant.objects.filter(beatwrituser__in=self.circle.all())
        writids = Participant.objects.exclude(beatwrituser__exact=self).values_list('writ', flat=True)
        writs = Writ.objects.filter(id__in=writids).order_by('-last_addition_date')[:count]
        return writs

    def get_absolute_url(self):
        return '/authors/%s' % self.id

    def get_nods_received(self):
        nods = Nod.objects.filter(receiver__id__exact=self.id).order_by('-date')
        return nods
    def get_nods_given(self):
        nods = Nod.objects.filter(giver__id__exact=self.id).order_by('-date')
        return nods
    def get_additions_count(self):
        return self.addition_set.count()
        
    def is_in_circle(self, bwuser):
        return bwuser in self.circle.all()

    def can_add_to_circle(self, bwuser_to_add):
        ids = map(lambda x: x.id, self.circle.all()[:])
        if bwuser_to_add.pk in ids:
            return ConditionList.ADD_TO_CIRCLE_FAIL__ALREADY_IN_CIRCLE 
        return ConditionList.ADD_TO_CIRCLE_SUCCESS
    
    def get_profile_visibility(self):
        if not self.profile_visibility:
            return 'none'
        else:
            return self.profile_visibility
    
    #TODO: remove this and test
    def pack(self):
        info = {}
        info['penname'] = self.get_penname()
        info['id'] = self.pk
        return info
    
    def get_nods_remaining(self):
        return self.nods_remaining
    
    def get_coauthors(self):
        #can be optimized later, make into a single SQL query
        writs = self.get_recent_writs(onlyactive=True)
        coauthors = []
        for w in writs:
            coauthors = coauthors + list(w.participants)
        return set(coauthors)

    def can_view_profile(self, bwuser):
        import main.access
        return main.access.AccessModel.can_access_profile(bwuser, self)

    def validate_penname(self, penname):
        if len(penname) < 3:
            return False
        return True

    #
    #   MODIFYING METHODS
    #
    def add_nods(self, count, save=True):
        self.nods_remaining = self.nods_remaining + count
        if save: self.save()

    def add_to_circle(self, bwuser_to_add):
        self.circle.add(bwuser_to_add)
        self.save()
    
    def set_addition_locales_cache(self, json_locales, pagenum, pagesize):
        d = {'pagenum':pagenum, 'pagesize':pagesize, 'locales':json_locales}
        self.addition_locales_cache = json.dumps(d)
        self.save()

    def get_addition_locales_cache(self):
        return json.loads(self.addition_locales_cache)

    def clear_addition_locales_cache(self):
        self.addition_locales_cache = ""
        self.save()
        


# Create your models here
class Writ(models.Model):
    creator = models.ForeignKey(BeatwritUser, related_name='created_writs')
    settings = models.OneToOneField('WritSettings', null=False)
    startdate = models.DateTimeField('Start date of Writ.', auto_now_add=True, editable=True)
    endeddate = models.DateTimeField(null=True, verbose_name='Ending date of Writ.  A null value means still in progress')
    participants = models.ManyToManyField(BeatwritUser, through='Participant')
    additions_count = models.IntegerField(default=0)                    #a cache of the number of additions in the writ
    ordering = models.TextField(default='[]')                                       #specification of the ordering (can change dynamically)
    content = models.TextField(default='')
    is_active = models.BooleanField(default=True)
    
    #the date of the last addition added
    last_addition_date = models.DateTimeField(auto_now_add=True)
    
    #the date of the last update of state
    last_update_date = models.DateTimeField(auto_now_add=True)
    total_view_count = models.IntegerField(default=0, db_index=True)
    total_nod_count = models.IntegerField(default=0, db_index=True)

    last_email_sent_to = models.ForeignKey(BeatwritUser, related_name='writs_emails_received', null=True)
    last_email_sent_at = models.DateTimeField(null=True)
    
    is_testing = models.BooleanField(default=False)
    
    #
    #   MODIFYING METHODS
    #
    def init(self, creator, settings, firstline, save=True):
        if firstline == '':
            raise WritValidityException("First line cannot be blank")
        self.creator = creator
        
        #Set the settings
        if settings:
            self.settings = settings
        else:
            ws = WritSettings()
            ws.save()
            if ws.endingtype == WritSettingsChoices.ending_type.TIME_LIMIT:
                ws.endingdate = datetime.now() + timedelta(14)
            ws.save()
            self.settings = ws
        self.save()
        
        if not self.settings.endingdate and self.settings.endingtype == WritSettingsChoices.ending_type.TIME_LIMIT:
            raise WritValidityException("Ending is set to 'timelimit' but ending date not given.")
        
        self.add_participant(creator, first=True)
        self.add_addition(creator, firstline)
        
        if save:
            self.save()
        print 'Writ %s created by %s' % (self.id, creator.id)
    
    def update_state(self):
        if self.check_is_finished():
            return
        
        #advance turns
        if not self.settings.turn_length == 0:
            time_diff = datetime.now() - self.lastupdatedate
            turns_to_skip  = int(utils.timedelta_to_minutes(time_diff) / self.settings.turn_length)
            if turns_to_skip > 0:
                self.advance_turns(turns_to_skip)

    def advance_turns(self, count):
        order = self._get_ordering_ids()
        for x in xrange(0, count):
            order.append(order.pop(0))
        self._set_ordering_ids(order, save=False)
        self.lastupdatedate = datetime.now()

        #THIS IS WHERE YOU SEND AN EMAIL
        bwuser_next = BeatwritUser.objects.get(id=long(order[0]))
        main.email.EmailManager.bwuser_begins_turn(bwuser_next, self)
        self.save()

        return bwuser_next


    def add_participant(self, bwuser, save=True, first=False, force=False ):
        res = self.can_join(bwuser)
        if not res.issuccess() and not first and not force:
            return res 
       
        try:
            #update seralized cache
            order = json.loads(self.ordering)
            order = [bwuser.id] + order
            self.ordering = json.dumps(order)

            p = Participant()
            p.beatwrituser = bwuser 
            p.order =  None
            p.writ = self
            p.save()
            if save:
                self.save()
            
            #Turn Policy while adding participants
            #   when a bwuser joins a writ, it automatically becomes their turn
            print 'Partipant %s added to %s' % (bwuser.id, self.id)
            return ConditionList.SUCCESS
        except:
            return ConditionList.FAIL

    
    #changed the default value of force to be False (might cause problems)
    def add_addition(self, bwuser, _content, force=False, save=True):
        content = utils.to_unicode(_content)
        if not force:
            self.validate_addition(bwuser, content)
        if len(content) == 0:
            raise WritValidityException("New addition cannot have empty content")
        
        is_last_space = False
        if len(self.content) > 0:
            if not self.content[-1] in '\n\t \r':
               content = ' ' + content 
        try:
            self.content = unicode(self.content) + unicode(content)
        except Exception, e:
            raise Exception(e)

        addition = Addition(writ=self, position=self.additions_count, author=bwuser, authorpenname=bwuser.get_penname(), content=content)
        
        import django.db
        try:
            addition.save()
        except django.db.IntegrityError, e:
            self.additions_count = self.addition_set.count()
            self.save()
            raise e
        

        self.additions_count = self.additions_count + 1
        self.last_addition_date = datetime.now()
        
        try:
            #if round-robin scheduling
            if self.settings.turn_type == WritSettingsChoices.turn_type.ROUND_ROBIN:
                self.advance_turns(1)
            #if free-for-all 
            elif self.settings.turn_type ==  WritSettingsChoices.turn_type.FREE_FOR_ALL:
                order = self._get_ordering_ids()
                order.append(order.pop(order.index(bwuser.pk)))
                self._set_ordering_ids(order, save=False)
                self.lastupdatedate = datetime.now()
                #self.save() does this need to be here?
            else:
                raise Exception ('Illegal turn_type stored: %s' % self.settings.turn_type)
        except Exception,e:
            if save:
                self.save()
            raise e
        
        print '%s ADDITION to %s by %s' % (self.additions_count+1, self.id, bwuser.id)
        if save:
            self.save()
        
        self.check_is_finished()
        return addition
    
    def _set_ordering_ids(self, uid_list, save=True):
        self.ordering = json.dumps(uid_list)
        self.validate_ordering(uid_list)
        if save:
            self.save()

    def close_writ(self):
       self.endeddate = datetime.now()
       self.is_active = False
       self.save()
        
    def increment_viewcount(self):
        self.total_view_count = self.total_view_count + 1
        self.save()

    def check_is_finished(self):
        if not self.endeddate:
            return True
        et = self.settings.endingtype 
        if et == et.choices.ending_type.WORD_LIMIT:
            if self.settings.wordlimit <= self.get_word_count():
                self.close_writ()
                return True
            else:
                return False
        elif et == et.choices.ending_type.TIME_LIMIT:
            if not self.settings.endingdate:
                pdb.set_trace()
            if self.settings.endingdate < datetime.now():
                self.close_writ()
                return True
            else: return False
        elif et == et.choices.ending_type.INACTIVITY:
            if self.get_last_addition_date() + timedelta(seconds=self.settings.inactive_time) <= datetime.now():
                self.close_writ()
                return True
            else:
                return False
        elif et == et.choices.ending_type.INACTIVE_ROUND:
            raise Exception('This needs to be implemented')
        else:
            raise Exception('Invalid value for endingtype: %s' % et)


    #
    #   READ-ONLY METHODS
    #
    def validate_addition(self, bwuser, content):
        if not self.endeddate is None:
            raise utils.WritValidityException("Cannot create new addition.  Writ when has ended.")
        #correct length
        if not self.is_valid_length(bwuser, content):
            s = "Cannot create new addition.  Content is too large. \Words: max-%s actual=%s\nContent: %s" % (self.settings.max_words_per_contribution, utils.find_word_count(content), content)
            print s 
            raise utils.WritValidityException(s)
        
        if not self.is_users_turn(bwuser):
            raise utils.WritValidityException("Cannot create new addition.  Turntype set to round-robin and it isn't the user's turn to contribute.")
        #is the content valid?
        #no illegal characters
        return True
    def __unicode__(self):
        return u"%s| %s" % (self.id, self.creator)

    def get_participant_count(self):
        return len(self.participants.all())

    def get_absolute_url(self):
        return '/writs/%s' % self.id

    def get_ending_string(self):
        if self.endeddate:
            return 'Finished'
        if self.settings.endingtype == WritSettingsChoices.ending_type.TIME_LIMIT:
            td = self.settings.endingdate - datetime.now()
            return utils.minutes_to_natural(td.seconds / 60, simple=True)
        elif self.settings.endingtype == WritSettingsChoices.ending_type.WORD_LIMIT:
            return "%s words" % self.get_words_remaining()
        elif self.settings.endingtype == WritSettingsChoices.ending_type.INACTIVITY:
            td = (self.get_last_addition_date() + timedelta(seconds=self.settings.inactive_time)) - datetime.now()
            return str(utils.minutes_to_natural(td.seconds / 60, simple=True)) + '*'
        elif self.settings.endingtype == WritSettingsChoices.ending_type.INACTIVE_ROUND:
            raise Exception("This needs to be implemented still")
        else:
            return self.settings.endingtype
    
    def get_words_remaining(self):
        if not self.settings.endingtype == WritSettingsChoices.ending_type.WORD_LIMIT:
            return None
        return self.settings.wordlimit - self.get_word_count()


    def get_first_line(self):
        adds = self.addition_set.filter(position__lt=5)
        content = ''
        for addition in adds:
            content = content + addition.content
            if len(content) > 140:
                return content
        return content
    def get_random_bwuser(self):
        parts = self.participants.all()
        return parts[randint(0, len(parts)-1)]
        
    def get_word_count(self):
        content = self.get_content()
        words = utils.split_words(content)
        return len(words)
    def get_whose_turn(self):
        uo = self.get_user_order()
        user = uo[0]
        return user
    def get_last_addition_date(self):
        if self.last_addition_date:
            return self.last_addition_date

        adds = self.addition_set.all().order_by('-position')
        return adds[0].date
    
    def _get_ordering_ids(self):
        return json.loads(self.ordering) 
    
    def get_user_order(self):
        ordering = self._get_ordering_ids()
        for i in xrange(0, len(ordering)):
            ordering[i] = BeatwritUser.objects.get(id=ordering[i])
        return ordering
    
    def get_content(self, nocache=True, debug=True):
        if debug or nocache or True:
            adds = None
            s = ''
            adds = self.addition_set
            adds = adds.order_by('position').all()
            for add in adds:
                if s != '':
                    if len(add.content) > 0:
                        if not s[-1] in (' ', '\n') and not add.content[0] in (' ', '\n'):
                            s = s + ' '
                if debug:
                    s = s + unicode(add)
                else: 
                    s = s + add.content
            return s
        elif self.content == '':
            return 'This writ has nothing in it.'
        else:
            log('This writ has someting')
            return self.content
        log('what? ')
        raise Exception('get_content didnt finish.')
    
    def validate_ordering(self, uid_list):
        count = 0
        for i in xrange(0, len(uid_list)):
            for j in xrange(0, len(uid_list)):
                if int(uid_list[i]) == int(uid_list[j]):
                    count = count + 1
                if count > 1:
                    s = "A number has occurred more than once in the ordering.\nordering = %s\nwritid = %s" % (self.ordering, self.id)
                    raise Exception(s)
            count = 0
    
    def get_users(self):
        parts_pks = self.partcicipants.values_list('pk', flat=True)
        return BeatwritUsers.objects.filter(pk__in=parts)[:]

    def is_users_turn(self, bwuser):
        order = self.get_user_order()
        if self.settings.turn_type == WritSettingsChoices.turn_type.ROUND_ROBIN:
            if order[0].pk != bwuser.pk:
                return False
        return True
    
    def is_valid_length(self, bwuser, content):
        max_words = self.settings.max_words_per_contribution
        if max_words > 0 and utils.find_word_count(content) > max_words:
            return False
        return True
    
    def is_users_turn_expired(self):
        addition = self.addition_set.order_by('-date').all()[0]
        if datetime.now() > addition.date + timedelta(minutes=self.settings.turn_length):
            return True
        return False
    
    def is_invited(self, bwuser):
        return True

    def is_in_circle_of_authors(self, bwuser):
        import main.access
        return main.access.AccessModel.can_access_writ(bwuser, self)
        
    def is_user_participant(self, bwuser):
        ids = map(lambda x: x.pk, self.participants.all()[:])
        return bwuser.pk in ids

    #Returns: a condition code
    def can_join(self, bwuser):
        if self.settings.who_can_join == WritSettingsChoices.who_can_join.INVITE_ONLY:
            if not self.is_invited(bwuser):
                return ConditionList.CANT_JOIN__INVITE_ONLY
        if self.settings.who_can_join == WritSettingsChoices.who_can_join.FRIENDS_ONLY:
            if not self.is_in_circle_of_authors(bwuser):
                return ConditionList.CANT_JOIN__ONLY_CIRCLE
        if self.is_user_participant(bwuser):
            return ConditionList.JOIN_FAIL__ALREADY_JOINED
        if self.settings.who_can_join == WritSettingsChoices.who_can_join.FULL_PUBLIC:
            pass
        return ConditionList.CAN_JOIN

    def can_view(self, bwuser):
        if bwuser in self.participants.all():
            return True

        if self.settings.public_visibility == WritSettingsChoices.public_visibility.FRIENDS:
            if not self.is_in_circle_of_authors(bwuser):
                return False
        elif self.settings.public_visibility == WritSettingsChoices.public_visibility.ONLY_AUTHORS:
            if not bwuser in self.participants.all():
                return False
        return True

class Participant (BeatwritModel):
    beatwrituser = models.ForeignKey(BeatwritUser)
    order = models.IntegerField(null=True)
    writ = models.ForeignKey(Writ)
    #nods_remaining = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s, %s' % (self.order, unicode(self.beatwrituser))

class Addition(BeatwritModel):
    writ = models.ForeignKey(Writ) 
    position = models.IntegerField()
    
    author = models.ForeignKey(BeatwritUser)
    authorpenname =  models.CharField(max_length=50, default='_')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
   
    #table denormalization
    total_nod_count = models.IntegerField(default=0, db_index=True)

    class Meta:
        unique_together = ('writ','position') 
    def __unicode__(self):
        return u"%s,%s:%s" % (self.author, self.position, self.content[:10])
    
    def is_new(self, user):
        bwu = user.beatwrituser
        most_recent_addition = self.writ.addition_set.filter(author__is=bwu).order_by('date')[-1]
        most_recent_position = most_recent_addition.position
        if self in self.writ.addition_set.filter(position_lt=most_recent_position).all():
            return True
        else:
            return False

    def pack(self):
        #pdb.set_trace()
        packed = super(type(self), self).pack()
        nods = self.nod_set.all()
       
        packed['penname'] = self.authorpenname
        packed['_reldate'] = utils.timedelta_from_now(self.date)
        
        #nods
        nodlist = []
        if not nods:
            nods = None
        else:
            for i in xrange(0, len(nods)):
                nodlist.append(nods[i].get_dict())
        packed['nods'] = nodlist
        return packed

    """def pack(self):
        nods = self.nod_set.all()
        nodlist = []
        if not nods:
            nods = None
        else:
            for i in xrange(0, len(nods)):
                nodlist.append(nods[i].get_dict())
        return {    
                    'id': self.pk,
                    'text': self.content,
                    'nods': nodlist,
                    'author' : self.author.pack(),
                    'writid' : self.writ.pk,
                    '_reldate': timedelta_to_natural(datetime.now() - self.date, simple=True)
               }
    """
    def get_absolute_url(self):
        return '/additions/%s' % self.id
    
    def can_nod(self, from_bwuser):
        return self.verify_can_nod(from_bwuser).issuccess()

    def verify_can_nod(self, from_bwuser):
        #can't give nods to self
        if self.author.pk == from_bwuser.pk:
            return ConditionList.NOD_FAIL__CANT_NOD_TO_SELF
        
        if from_bwuser.nods_remaining < 1:
            return ConditionList.NOD_FAIL__NO_NODS_TO_GIVE

        #Can't nod to the same addition twice
        for nod in self.nod_set.all():
            if nod.giver.pk == from_bwuser.pk:
                return ConditionList.NOD_FAIL
        return ConditionList.SUCCESS

    #Called to give a nod to this addition  
    def make_nod(self, from_bwuser):
        try:
            n = Nod()
            n.giver = from_bwuser
            n.receiver = self.author
            n.addition = self
            n.writ = self.writ
            n.save()
        except:
            return ConditionList.NOD_FAIL

        return ConditionList.NOD_SUCCESS

    def save(self, *args, **kwargs):
        creating = True if self.pk else False
        super(Addition, self).save(*args, **kwargs)
        if creating:
            self.author.total_additions = self.author.total_additions + 1
            self.author.clear_addition_locales_cache()
            self.author.add_nods(1, save=False) 
            self.author.save()

class Nod(BeatwritModel):
    giver = models.ForeignKey(BeatwritUser, related_name='nodsgiven')
    receiver = models.ForeignKey(BeatwritUser, related_name='nodsreceived')
    addition = models.ForeignKey(Addition)
    writ = models.ForeignKey(Writ)
    date = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return u"%s, %s" % (self.giver.get_penname(), self.receiver.get_penname())
    def get_dict(self):
        return {'giver': self.giver.pack(),
                'receiver': self.receiver.pack(),
                'addition': self.addition.pk,
                'date': unicode(self.date)
                }
    def get_absolute_url(self):
        return '/nods/%s' % self.id
    
    def save(self, *args, **kwargs):
        cond = self.addition.verify_can_nod(self.giver)
        if not cond.issuccess():
            raise Exception("%s | %s" % (self.giver,cond.message))
        super(Addition, self).save(*args, **kwargs)
        
        self.giver.nods_remaining = self.giver.nods_remaining - 1
        
        #Every time you receive a nod from another player, your available nods to give increases
        self.receiver.add_nods(1,save=True)
        
        #Increment the totalnodcount cache
        self.writ.total_nod_count = self.writ.total_nod_count + 1
        self.writ.save()


class WritInvite(BeatwritModel):
    writ = models.ForeignKey(Writ)
    fromuser = models.ForeignKey(BeatwritUser,db_index=True,  related_name='writ_invites_given', editable=False)
    touser = models.ForeignKey(BeatwritUser,db_index=True, related_name='writ_invites_received', editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return u"%s, %s" % (self.fromuser, self.date)
    def get_absolute_url(self):
        return '/writinvites/%s' % self.id

class CircleInvite(BeatwritModel):
    writ = models.ForeignKey(Writ)
    fromuser = models.ForeignKey(BeatwritUser, db_index=True, related_name='circle_invites_given', editable=False)
    touser = models.ForeignKey(BeatwritUser, db_index=True, related_name='circle_invites_received', editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    ignored = models.BooleanField()
    accepted = models.BooleanField()
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return u"%s, %s" % (self.fromuser, self.date)
    def get_absolute_url(self):
        return '/circleinvites/%s' % self.id

#This class isn't fully implemented
class LoginToken(BeatwritModel):
    token = models.BigIntegerField (editable=False, db_index=True, default=utils.random_positive_long)
    expiration = models.DateTimeField(default=utils.week_from_now)
    user = models.ForeignKey(django.contrib.auth.models.User, db_index=True)
    is_active = models.BooleanField(default=True)
    
class EmailChangeToken(BeatwritModel):
    token = models.BigIntegerField (editable=False, default=utils.random_positive_long)
    expiration = models.DateTimeField(default=utils.week_from_now)
    bwuser = models.ForeignKey(BeatwritUser, editable=False)
    email = models.EmailField(editable=False)

class EmailToSend(BeatwritModel):
    bwuser = models.ForeignKey(BeatwritUser, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    email = models.EmailField(editable=False)
    args = models.TextField(blank=True)
    template = models.CharField(max_length=50)
    sendafter = models.DateTimeField()
    expiresafter = models.DateTimeField()

class WritSettingsChoices:
    who_can_join = enum_ex(
                            (0,'FULL_PUBLIC','Anyone can join this writ.','public'),
                            (1, 'INVITE_ONLY','Authors can only join by invite.','invite'),
                            (2, 'FRIENDS_ONLY', 'Only those in the circle of the authors can join','circle'),)
    ending_type = enum_ex(
                            (0, 'WORD_LIMIT','The writ ends after a specified number of words has been reached.','word limit'),
                            (1, 'TIME_LIMIT','The writ ends after a specified time limit has past.','time limit'),
                            (2, 'INACTIVITY','The writ ends after a specified time of inactivity','inactivity'),
                            (3, 'INACTIVE_ROUND','The writ ends after every author has passed their turn.','inactive round'),)
    turn_type = enum_ex(
                            (0, 'FREE_FOR_ALL','Any author is free to contribute at any time.','free for all'),
                            (1, 'ROUND_ROBIN','Authors take turns contributing in order.','round robin'))
    public_visibility = enum_ex(
                                (0, 'FRIENDS','Only those in the circle of the authors can see the writ.','circle'),
                                (1, 'ONLY_AUTHORS', 'Only the authors can see the writ.','authors'),
                                (2, 'FULL_PUBLIC', 'The writ is viewable by anyone.','public'))

class WritSettings(BeatwritModel):
    choices = WritSettingsChoices

    CONTRIB_SIZE_CHOICES = (
        (1,'One word'),
        (5,'Phrase (5 words)'),
        (15 ,'Short sentence (15 words)'),
        (25 ,'Sentence (25 words)'),
        (60,'Paragraph (60 words)',),
        (0,'Unlimited',),
    )

    TURN_LENGTH_CHOICES = (
        (1440, 'blitz (1 day)'),
        (4320, 'casual (3 days)'),
        (0, 'unlimited'),
    )

    WHO_CAN_JOIN_CHOICES = (
        (choices.who_can_join.FULL_PUBLIC,choices.who_can_join.l.FULL_PUBLIC ),
        (choices.who_can_join.INVITE_ONLY,choices.who_can_join.l.INVITE_ONLY),
        (choices.who_can_join.FRIENDS_ONLY,choices.who_can_join.l.FRIENDS_ONLY),
    )
    ENDING_TYPE_CHOICES = (
        (choices.ending_type.WORD_LIMIT,choices.ending_type.l.WORD_LIMIT),
        (choices.ending_type.TIME_LIMIT,choices.ending_type.l.TIME_LIMIT),
        (choices.ending_type.INACTIVITY,choices.ending_type.l.INACTIVITY),
        (choices.ending_type.INACTIVE_ROUND,choices.ending_type.l.INACTIVE_ROUND),
    )

    WORDLIMIT_CHOICES = (
        (150,'Short (150 words)'),
        (400,'Medium (400 words)'),
        (800,'Long (800 words)'),
    )
    TURN_TYPE_CHOICES = (
        (choices.turn_type.FREE_FOR_ALL,choices.turn_type.l.FREE_FOR_ALL),
        (choices.turn_type.ROUND_ROBIN,choices.turn_type.l.ROUND_ROBIN),
    )
    PUBLIC_VISIBILITY_CHOICES = (
        (choices.public_visibility.FRIENDS,choices.public_visibility.l.FRIENDS),
        (choices.public_visibility.FULL_PUBLIC,choices.public_visibility.l.FULL_PUBLIC),
        (choices.public_visibility.ONLY_AUTHORS,choices.public_visibility.l.ONLY_AUTHORS),
    )

    def save(self):
        #make sure the inputs make sense
        error = ''
        if self.endingtype == self.choices.ending_type.TIME_LIMIT  and not self.endingdate:
            error = "Endingtype is 'timelimit' yet no endingdate is given"
        elif self.endingtype == self.choices.ending_type.WORD_LIMIT and not self.wordlimit:
            error = "Endingtype is 'wordlimit' yet no wordlimit is given"
        elif self.endingtype == self.choices.ending_type.INACTIVITY and not self.inactive_time:
            error = "Endingtype is 'inactivity' yet no inactive time is given"

        if error:
            raise WritSettingsValidityException(error)
        super(WritSettings, self).save() # Call the "real" save() method

    ht = "Size of contribution: Sentence, paragraph, unlimited"
    max_words_per_contribution = models.SmallIntegerField(help_text=ht, default=25, )

    def contribution_size_string(self, short=True):
        max_words = int(self.max_words_per_contribution)
        try:
            d = None
            for x in self.CONTRIB_SIZE_CHOICES:
                if x[0] == max_words:
                    if short:
                        return x[2]
                    else:
                        return x[1]
            return d[max_words]
        except:
            return '%s words' % max_words


    ht = "Length of time (in minutes) a participant has to contribute before turn is forfeitted."
    turn_length = models.PositiveIntegerField(help_text=ht, default=1440,)

    def get_turn_length(self):
        if True:
            return minutes_to_natural(self.turn_length)
        if self.turn_length == 60:
            return 'blitz'
        if self.turn_length == 1440:
            return 'casual'
        if self.turn_length == 0:
            return 'unlimited'
        else:
            #td = datetime.timedelta(minutes=self.turn_length)
            return minutes_to_natural(self.turn_length)
    
    ht = "Is invite only?  Choices: invite-only, only friends, full public"
    who_can_join = models.PositiveSmallIntegerField(help_text=ht, default=choices.who_can_join.INVITE_ONLY, choices=WHO_CAN_JOIN_CHOICES, max_length=15)
    
    #
    # TODO: CONVERT ENDINGTYPE TO BE A SMALLINTEGER FIELD
    #
    ht = "When does the writ end? Choices: TIME_LIMIT, WORD_LIMIT, INACTIVITY"
    endingtype = models.CharField(help_text=ht, default=choices.ending_type.INACTIVE_ROUND,max_length=15, choices=ENDING_TYPE_CHOICES)
    
    ht = "How many words before the writ ends? (only for endingtype=wordlimit)"
    wordlimit = models.PositiveSmallIntegerField(help_text=ht, null=True)
    
    ht = "The number of days of inactivity before a writ is closed. (in seconds)"
    inactive_time = models.PositiveIntegerField(help_text=ht, null=True)
    endingdate = models.DateTimeField(help_text='Is null if endingtype is not time-limit', null=True, default=lambda: datetime.now() + timedelta(days=30))
    def public_visibility_string(self):
        for x in self.PUBLIC_VISIBILITY_CHOICES:
            if x[0] == self.public_visibility:
                return x[1]
        return "String not found"
    
    def who_can_join_string(self):
        for x in self.WHO_CAN_JOIN_CHOICES:
            if x[0] == self.who_can_join:
                return x[1]
        return "String not found"
    
    def turn_length_string(self):
        for x in self.TURN_LENGTH_CHOICES:
            if x[0] == self.turn_length:
                return x[1]
        #return "%s minutes" % self.turn_length
        return minutes_to_natural(self.turn_length)

    def turn_type_string(self):
        for x in self.TURN_TYPE_CHOICES:
            if x[0] == self.turn_type:
                return x[1]
        return "String not found"
        
    def get_ending_point (self):
        #pdb.set_trace()
        if self.endingtype == self.choices.ending_type.TIME_LIMIT:
            return timeuntil(self.endingdate)
        elif self.endingtype == self.choices.ending_type.WORD_LIMIT:
            return self.wordlimit
        elif self.endingtype == self.choices.ending_type.INACTIVITY:
            d = self.writ.get_last_addition_date()
            dt = timedelta(seconds=self.inactive_time)
            return d + dt
        elif self.endingtype == self.choices.ending_type.INACTIVE_ROUND:
            return 'all players consecutively pass their turn'
        else:
            return self.endingtype 
    ht = "Is the writ publically browsable.  Can the writ be seen by others not connected with the authors.  Will it be listed in the public direcories of writs once it is finished."
    public_visibility = models.PositiveSmallIntegerField(help_text=ht, default=choices.public_visibility.FRIENDS, choices=PUBLIC_VISIBILITY_CHOICES, max_length=15)
    
    ht = "How do participants take turns?  Choices: freeforall, roundrobin"
    turn_type = models.PositiveSmallIntegerField(help_text=ht, default=choices.turn_type.ROUND_ROBIN, max_length=20, choices=TURN_TYPE_CHOICES)

    def get_turn_type(self): 
        if self.turn_type == WritSettingsChoices.turn_type.ROUND_ROBIN:
            return 'Round-robin'
        elif self.turn_type == WritSettingsChoices.turn_type.FREE_FOR_ALL:
            return 'Free-for-all'
        else:
            return self.turn_type   
    
    extra = models.TextField(blank=True)    

    def __unicode__(self):
        if self.writ:
            return u'WS| writid: %s' % self.writ.id
        else:
            return u'WS| writid: none' 

"""
Is Writ publically browsable?

Writ Parameters:
Contribution
    -max words per 
    -formatting allowed? (of course it's allowed)

-Max hours/days before turn is forfeited

Joining writ:
    only invitees
    full public

Turn-types:
    strict roundrobin
    free for all

Ordering (future):
    normal -- contribution only at end
    anywhere -- contributions can be made anywhere in writ

Inspiration:
    Image
        Select the most interesting creative commons image from flickr
    Starting text is juicy passage from an old book; participants continue
    Vocabulary expansion:
        must incorporate the word of the day into contribution
    Sound
    
Personal Options
    penname
    display link to facebook profile?

Feature:
    chat/comments per each writ

Other games (future):
    Madlibs
    Word association
"""




"""
    User logged in  |   Is user participant |   Is Users turn   |   User has Nods    |  Writ is closed
"""



"""
    max_words_per_contribution 
        X Backend: make sure posts don't have greater
        _not needed?_ Javascript: make sure posts don't have greater
    turn_length
        X update_state: If turn expired, update turn ordering
    who_can_join
        Backend: verify_can_join
    endingtype
        update_state: check_has_ended
    
    public_visibility
        Backend: Show 'writ is private' template 
    
    turn_type = models.CharField(help_text=ht, default='rr', max_length=20, choices=TURN_TYPE_CHOICES)

"""
