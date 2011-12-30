import datetime
import django.contrib.auth.models
from django import forms
from models import *
from django.contrib.auth.models import User

DAYS_OPEN_CHOICES = (
    (3,'3 days'),
    (7,'7 days'),
    (14,'2 weeks'),
)

PROFILE_VISIBILITY_CHOICES = (
    (str(BeatwritUserChoices.profile_visibility.ONLY_CIRCLE) ,'Only Circle'),
    (str(BeatwritUserChoices.profile_visibility.FULL_PUBLIC),'Everyone'),
    (str(BeatwritUserChoices.profile_visibility.ONLY_AUTHOR),'Only Author'),
)

class EmailChangeForm(forms.Form):
    emailaddress = forms.EmailField(label="Enter your email if you would like to receive emails reminding you when it is your turn.",
                                    required=False)
    @classmethod
    def default (cls, bwuser):
        return EmailChangeForm(initial={'emailaddress':bwuser.authuser.email})


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'id':'password'}))
    password1 = forms.CharField(label="", widget = forms.PasswordInput(attrs={'id':'password1'}))
    password2 = forms.CharField(label="", widget = forms.PasswordInput(attrs={'id':'password2'}))

    @classmethod
    def default(cls, bwuser=None):
        return PasswordChangeForm()

    def process(self):
        if len(password1.strip()) > 0:
            if (password2.strip() == 0):
                raise Exception ("Please enter password twice to verify a match.")

class OptionsChangeForm(forms.Form):
    REMINDERS_DISABLED_CHOICES = [  ('disabled',"Don't send me reminders"),
                                    ('enabled', "Send me reminders when it's my turn")]
    
    EMAIL_INVITES_CHOICES = [   ('disabled',"Don't send me emails when I'm invited to a writ"),
                                ('enabled', "Emails for invites are okay")]
    
    penname = forms.CharField(  label="How do you want others to see you?",
                                required=True)
    
    email_reminders = forms.ChoiceField(  label="Do you want to receive email reminders when it is your turn?",
                                            choices=REMINDERS_DISABLED_CHOICES,
                                            widget=forms.RadioSelect, 
                                            required=True,
                                            initial='disabled')

    email_invites = forms.ChoiceField(  label="Do you want to receive an email when you are invited to join a new writ?",
                                                choices=EMAIL_INVITES_CHOICES,
                                                widget=forms.RadioSelect, 
                                                required=True,
                                                initial='disabled')

    profile_visibility = forms.ChoiceField(  label="Who should be able to see your profile?",
                                            choices=BeatwritUser.PROFILE_VISIBILITY_CHOICES,
                                            widget=forms.RadioSelect, 
                                            required=True,
                                            initial='0')

    surfaceable_additions = forms.BooleanField(label="Allow my public contributions to be featured.") 

    @classmethod
    def default(cls, bwuser):
        initial = {'penname':bwuser,
                    'email_reminders': 'enabled' if bwuser.email_reminders_enabled else 'disabled',
                    'email_invites' : 'enabled' if bwuser.email_invites_enabled else 'disabled',
                    'profile_visibility' : bwuser.profile_visibility,
                    'surfaceable_additions' : bwuser.additions_surfacable,
                    }
        return OptionsChangeForm(initial=initial)

    def save_settings(self, bwuser):
        d = self.cleaned_data
        if not d:
            return

        if bwuser.validate_penname(d['penname']):
            bwuser.penname = d['penname']
        
        if d['email_invites'] == 'enabled':
            bwuser.email_invites_enabled = True
        elif d['email_invites'] == 'disabled':
            bwuser.email_invites_enabled = False 
        
        if d['email_reminders'] == 'enabled':
            bwuser.email_reminders_enabled = True
        elif d['email_reminders'] == 'disabled':
            bwuser.email_reminders_enabled = False 
        
        #if d['profile_visibility'] == str(BeatwritUserChoices.public_visibility.FULL_PUBLIC)):
        val = int(d['profile_visibility'])
        if BeatwritUserChoices.profile_visibility.isvalid(val):
            bwuser.profile_visibility = val
        bwuser.additions_surfaceable = d['surfaceable_additions']
        bwuser.save()


class NewWritForm(forms.Form):
    WHO_CAN_JOIN_CHOICES = (
        (0,'Anyone can join this writ.','public'),
        (2, 'Only those in the circle of the authors can join','circle'),
    )
    
    public_visibility = (
        (0, 'FRIENDS','Only those in the circle of the authors can see the writ.','circle'),
        (1, 'ONLY_AUTHORS', 'Only the authors can see the writ.','authors'),
        (2, 'FULL_PUBLIC', 'The writ is viewable by anyone.','public')
    )

    openingline = forms.CharField(label="How should the writ start?", widget=forms.Textarea)

    turn_length = forms.ChoiceField(label="How long in should authors have before their turn is passed to the next person?", widget=forms.RadioSelect, choices=WritSettings.TURN_LENGTH_CHOICES, initial='1440')

    max_words_per_contribution = forms.ChoiceField(label="How much should authors be able to contribute per turn?", widget=forms.RadioSelect, choices=WritSettings.CONTRIB_SIZE_CHOICES, initial='25')

    who_can_join = forms.ChoiceField(label="Do you want to limit who is able to join the writ?", widget=forms.RadioSelect, choices=WHO_CAN_JOIN_CHOICES, initial='fullpublic')

    endingtype = forms.ChoiceField(label="How do you want the writ to end?", widget=forms.RadioSelect, choices=WritSettings.ENDING_TYPE_CHOICES, initial='wordlimit', required=False)

    wordlimit = forms.ChoiceField(label='How many words before the writ closes?', choices=WritSettings.WORDLIMIT_CHOICES, required=False)

    days_open = forms.ChoiceField(label='How many days will the writ be open?', widget=forms.RadioSelect, choices=DAYS_OPEN_CHOICES, required=False)

    public_visibility = forms.ChoiceField(label="Should the writ be publically viewable?", widget=forms.RadioSelect, choices=WritSettings.PUBLIC_VISIBILITY_CHOICES, initial='onlyfriends')

    inactive_time = forms.IntegerField(label='How many turns skipped before writ is closed due to inactivity?', required=False)

    def _make_writ_settings(self):
        d = self.cleaned_data
        ws = WritSettings()
        ws.turn_length = d['turn_length']
        ws.max_words_per_contribution = d['max_words_per_contribution']
        ws.who_can_join = d['who_can_join']

        if d['public_visibility']:
            ws.public_visibility = d['public_visibility']
        
        if d['endingtype']:
            ws.endingtype = d['endingtype']
        else:
            ws.endingtype = 'inactiveround'
        if d['endingtype'] == 'timelimit':
            ws.endingdate = datetime.timedelta(days=['self.days_open']) + datetime.datetime.now()
        elif d['endingtype'] == 'wordlimit':
            ws.wordlimit = d['wordlimit']
        elif d['endingtype'] == 'inactivity':
            ws.inactive_time = d['inactive_time_days'] * 3600 * 24
        ws.save()
        return ws
    def make_writ(self, bwuser):
        d = self.cleaned_data
        w = Writ()
        ws = self._make_writ_settings()
        print 'Making new writ %s' % str(d)
        w.init(bwuser, ws, d['openingline'])
        w.save()
        return w
            
class NewUserForm(forms.Form):
    """
    Receieves input from the user and outputs a new user object. 
    ""
    
    """
        
    username_f = forms.CharField(label='Username:') 
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm:', widget=forms.PasswordInput)
   
    """  The penname is how other users will see you on the site.  It doesn't have to be unique and you can change it later."""
    penname = forms.CharField(label="Penname:")
    
    """  Giving your email address is optional, but it gives you two advantages: 1) The insurance against forgetting your password 2) The ability to opt in to turn reminder emails."""
    email = forms.EmailField(label='Email (optional):', required=False)
    def is_username_taken(self):
        if not self.is_bound:
            return False
        u = self.cleaned_data['username_f']
        if User.objects.filter(username=u).exists():
            return True 
        return False 
    def is_username_invalid(self):
        if not self.is_bound:
            return False
        u = self.cleaned_data['username_f']
        if not u:
            return False
        if not re.match(r'[a-zA-Z0-9_]{4,15}', u):
            return True 
        return False 
    def are_passwords_invalid(self):
        if not self.is_bound:
            return False
        d = self.cleaned_data
        if d['password1'] != d['password2'] and len(d['password1']) > 3:
            return True
        return False
    def make_user(self):
        d = self.cleaned_data 
        password1 = d['password1']
        password2 = d['password2']
        if password1 != password2:
            raise Exception("Passwords do not match.")
        
        user = django.contrib.auth.models.User.objects.create_user(d['username_f'], '', password1) 
        user.is_superuser = False
        user.is_staff = False
        user.save()
        #d['email']

        bwu = BeatwritUser()
        bwu.penname = d['penname']
        bwu.facebookid = None
        bwu.authuser = user
        bwu.nods_remaining = 0
        bwu.save()
        return bwu


"""
ORDER 
    
    
    P1
        max_words_per_contribution 
        openingline

    P2
        turn_length 
        endingtype 
            wordlimit 
            endingdate 
            inactive_time_days 
        public_visibility 
        who_can_join
    P3
        Invite friends 
            facebook
            recent co-authors
            email addresses
    """
