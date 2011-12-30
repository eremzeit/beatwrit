import json
from datetime import datetime
import random


"""
class FacebookUser(models.Model):
    facebookid = models.IntegerField(blank=True, null=True, verbose_name='Facebook User ID')
    name = models.CharField(max_length=50, verbose_name="User's Full Name")
    receivedinvites = models.ForeignKey('Invite', null=True, blank=True, verbose_name="Invites Received")
    careermedals = models.ManyToManyField('Medal', null=True, blank=True, verbose_name="Career Medals Received")
    timestamp = models.DateTimeField(auto_now=True, null=True)
    extra = models.TextField(blank=True)    
    def __unicode__(self):
        return self.name

# Create your models here
class Writ(models.Model):
    creator = models.ForeignKey(FacebookUser, related_name='createdlitlets')
    participant = models.ForeignKey(FacebookUser, null=True, related_name='coauthoredlitlets')
    title = models.TextField(blank=True, null=True)
    ordering = models.TextField(blank=True)
    options = models.OneToOneField('WritParams', null=True, blank=True)
    startdate = models.DateTimeField('Start date of Writ.', auto_now_add=True, editable=True)
    enddate = models.DateTimeField('Ending date of Writ.  A blank value means still in progress')
    timestamp = models.DateTimeField(auto_now=True)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return "<Writ| %s, %s, %s" % (self.creator, self.title, self.startdate)

class Addition(models.Model):
    author = models.ForeignKey(FacebookUser, related_name='authored_additions')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    content = models.TextField(blank=True)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return "<Addition | by %s, content: %s" % (self.author, self.content)

class Nod(models.Model):
    giver = models.ForeignKey(FacebookUser)
    addition = models.ForeignKey(Addition)
    date = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return "<Nod| from: %s, %s" % (self.giver, self.date)


class Invite(models.Model):
    litlet = models.ForeignKey(Writ)
    fromuser = models.ForeignKey(FacebookUser)
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    extra = models.TextField(blank=True)    
    
    def __unicode__(self):
        return "<Invite| from: %s, %s" % (self.fromuser, self.date)


class WritParams(models.Model):
    ht = "The type of Writ: story, poem, freeform, etc.."
    _default = 'story'
    writtype = models.CharField(max_length=20, default=_default, help_text=ht)

    ht = "The number of words allowed in a contribution" 
    _default = 40
    max_words_per_contribution = models.IntegerField(help_text=ht, default=_default)
    
    ht = "The length of time, in days, to wait in order to allow invited users to join litlet"
    _default = 3
    joining_period_days = models.IntegerField(help_text=ht, default=_default)

    ht = "The length of time (in days) that a coauthor is allowed to wait to submit a contribution before the coauthor's turn is forfeited"
    _default = 3
    max_turn_length_days = models.IntegerField(help_text=ht, default=_default)

    ht = "Although this is entirely optional, you may enter a short suggestion for the direction or plot of the Writ.  This suggestion may help to give inspiration to the coauthors on how to add to the Writ.  However, specifying a direction may have the negative effect of hindering the creativity of coauthors so use this feature with caution."
    _default = ''
    blurb_plot_summary = models.TextField(help_text=ht, default=_default)

    ht = "Specify here whether you would like to allow users to join as coauthors once the litlet is in progress."
    _default = False
    can_join_in_progress = models.BooleanField(help_text=ht, default=_default)

    ht = ""
    _default = False
    is_invite_only = models.BooleanField(help_text=ht, default=_default)

    ht = "Select this option if you would like to allow simple formatting to be used in the Writ."
    _default = False
    allow_rtf_formatting = models.BooleanField(help_text=ht, default=_default)
    extra = models.TextField(blank=True)    
"""
"""

Writ Parameters:
-max words per contribution
-Length of joining period, in days
-Max days before turn is forfeited
-Writ type: story, poem, freeform
-Blurb plot summary (optional)
	50 words or less describing the plot
-Are users allowed to join once the litlet has started?
-Is anyone allowed to join the litlet or only those who are invited?


Writ
	creator
    participants
	ordering
	options
	startdate
	enddate
	additions

Addition
	facebookuser
	content
	postdate

FacebookUser
	name
	ratings
"""
