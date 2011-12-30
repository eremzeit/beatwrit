from django.db import models
from datetime import datetime

class FacebookUser(models.Model):
    facebookid = models.IntegerField(blank=True, null=True, verbose_name='Facebook User ID')
    name = models.CharField(max_length=50, verbose_name="User's Full Name")
    receivedinvites = models.ForeignKey('Invite', null=True, blank=True, verbose_name="Invites Received")
    careermedals = models.ManyToManyField('Medal', null=True, blank=True, verbose_name="Career Medals Received")
    availmedals = models.IntegerField(default=0, verbose_name='Medals to Give')
    timestamp = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        return self.name

# Create your models here
class Litlet(models.Model):
    creator = models.ForeignKey(FacebookUser, related_name='createdlitlets')
    coauthor = models.ForeignKey(FacebookUser, null=True, related_name='coauthoredlitlets')
    title = models.CharField(max_length=50, blank=True)
    ordering = models.TextField(blank=True)
    options = models.OneToOneField('LitletParams', null=True, blank=True)
    startdate = models.DateTimeField('Start date of Litlet.', auto_now_add=True, editable=True)
    enddate = models.DateTimeField('Ending date of Litlet.  A blank value means still in progress')
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "<Litlet| %s, %s, %s" % (self.creator, self.title, self.startdate)

class Line(models.Model):
    author = models.ForeignKey(FacebookUser, related_name='authored_lines')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    content = models.TextField(blank=True)
    
    def __unicode__(self):
        return "<Line| by %s, content: %s" % (self.author, self.content)

class Medal(models.Model):
    giver = models.ForeignKey(FacebookUser)
    line = models.ForeignKey(Line)
    date = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        return "<Medal| from: %s, %s" % (self.giver, self.date)


class Invite(models.Model):
    litlet = models.ForeignKey(Litlet)
    fromuser = models.ForeignKey(FacebookUser)
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        return "<Invite| from: %s, %s" % (self.fromuser, self.date)


class LitletParams(models.Model):
    ht = "The type of Litlet: story, poem, freeform, etc.."
    _default = 'story'
    type = models.CharField(max_length=20, default=_default, help_text=ht)

    ht = "The number of words allowed in a contribution" 
    _default = 40
    max_words_per_contribution = models.IntegerField(help_text=ht, default=_default)
    
    ht = "The length of time, in days, to wait in order to allow invited users to join litlet"
    _default = 3
    joining_period_days = models.IntegerField(help_text=ht, default=_default)

    ht = "The length of time (in days) that a coauthor is allowed to wait to submit a contribution before the coauthor's turn is forfeited"
    _default = 3
    max_turn_length_days = models.IntegerField(help_text=ht, default=_default)

    ht = "Although this is entirely optional, you may enter a short suggestion for the direction or plot of the Litlet.  This suggestion may help to give inspiration to the coauthors on how to add to the Litlet.  However, specifying a direction may have the negative effect of hindering the creativity of coauthors so use this feature with caution."
    _default = ''
    blurb_plot_summary = models.TextField(help_text=ht, default=_default)

    ht = "Specify here whether you would like to allow users to join as coauthors once the litlet is in progress."
    _default = False
    can_join_in_progress = models.BooleanField(help_text=ht, default=_default)

    ht = ""
    _default = False
    is_invite_only = models.BooleanField(help_text=ht, default=_default)

    ht = "Select this option if you would like to allow simple formatting to be used in the Litlet."
    _default = False
    allow_rtf_formatting = models.BooleanField(help_text=ht, default=_default)
"""

Litlet Parameters:
-max words per contribution
-Length of joining period, in days
-Max days before turn is forfeited
-Litlet type: story, poem, freeform
-Blurb plot summary (optional)
	50 words or less describing the plot
-Are users allowed to join once the litlet has started?
-Is anyone allowed to join the litlet or only those who are invited?


Litlet
	creator
    participants
	ordering
	options
	startdate
	enddate
	lines

Line
	facebookuser
	content
	postdate

FacebookUser
	name
	ratings
"""
