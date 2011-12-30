from templates import *

from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives 
from datetime import datetime, timedelta

from tokens import TokenManager

TEST_EMAIL = 'erem.gumas@gmail.com'

class EmailManager:
    is_sending_enabled = True 
    is_realtime_mode = True
    
    @classmethod
    def bwuser_begins_turn(cls, bwuser, writ):
        if not bwuser.email_reminders_enabled or not cls.is_sending_enabled:
            return
        if cls.is_realtime_mode:

            context = {
                'penname':bwuser.get_penname(),
                'first_line':writ.get_first_line(),
                'direct_login_link': TokenManager.make_autologin_url(bwuser.authuser, writ.get_absolute_url()),
            }

            rec = None
            if writ.is_testing:
                rec = [TEST_EMAIL]
            else:
                rec = [bwuser.authuser.email]
            
            m = make_email_message(rec, 'turn_reminder', context)
            if m: m.send()
            
            writ.last_email_sent_to = bwuser
            writ.last_email_sent_at = datetime.now()
            writ.save()

    
    @classmethod
    def writ_inactive(cls, writ):
        if writ.settings.turn_type == writ.settings.choices.turn_type.FREE_FOR_ALL: 
            delay_interval = timedelta(seconds=writ.settings.inactive_time / 4)
            if datetime.now() - writ.last_email_sent_at > delay_interval:
                bwuser = writ.get_random_bwuser()
                while bwuser.pk == writ.last_email_sent_to.pk:
                    bwuser = writ.get_random_bwuser()
                
                if not bwuser.email_reminders_enabled or not cls.is_sending_enabled:
                    return
                rec = None
                if writ.is_testing:
                    rec = [TEST_EMAIL]
                else:
                    rec = [bwuser.authuser.email]
                if cls.is_realtime_mode:
                    context = {
                        'penname':bwuser.get_penname(),
                        'first_line':writ.get_first_line(),
                        'direct_login_link': TokenManager.make_autologin_url(authuser, writ.get_absolute_url()),
                    }

                    m = make_email_message(rec, 'turn_reminder', context)
                    m.send()
                    writ.last_email_sent_to = bwuser
                    writ.last_email_sent_at = datetime.now()
                    writ.save()
            
        elif writ.settings.turn_type == writ.settings.choices.turn_type.ROUND_ROBIN: 
            raise Exception("Invalid turn type.") 


def make_email_message(recipients, template_name, context, **kwargs):
    if not template_name in templates:
        print 'template not found'
        return
    email_strings = templates[template_name]
    
    #s = template.render(Context({}))
    subject = Template(email_strings ['subject']).render(Context(context))
    body_plain = Template(email_strings ['body_plain']).render(Context(context))
    body_html = Template(email_strings ['body_html']).render(Context(context))
    from_email = Template(email_strings ['from_email']).render(Context(context))
    
    err = filter(lambda x: x, [subject, body_plain, body_html, from_email])
    if err:
        print 
        print 'Not all email parts were created successfully'
     

    msg = EmailMultiAlternatives(subject, body_plain, from_email, recipients, **kwargs)
    msg.attach_alternative(body_html ,'text/html')
    return msg


def test_turn_reminder():
    template_name = 'turn_reminder' 
    c = {'penname': 'erem gumas', 'first_line': 'Once upon a midnight dreary', 'direct_login_link': 'http://beatwrit.com/writs/1'} 
    m = BeatwritEmailManager.make_email_message([TEST_EMAIL], template_name, c)
    m.send()

def test_inactive_reminder():
    template_name = 'inactive_reminder' 
    c = {'penname': 'erem gumas', 'first_line': 'Once upon a midnight dreary', 'direct_login_link': 'http://beatwrit.com/writs/1'} 
    m = BeatwritEmailManager.make_email_message([TEST_EMAIL], template_name, c)
    m.send()

def test_email_confirm():
    template_name = 'email_confirmation' 
    c = {'penname': 'erem gumas', 'email_confirm_url': 'http://www.example.com'} 
    m = BeatwritEmailManager.make_email_message([TEST_EMAIL], template_name, c)
    m.send()

def test_html_email():
    msg = EmailMultiAlternatives('test_subject', 'This is the plain body', 'no-reply@beatwrit.com', ['erem.gumas@gmail.com'])
    msg.attach_alternative(test_body_html2 ,'text/html')
    msg.send()
