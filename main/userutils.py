import sys
import beatwrit.settings

from conditions import ConditionList as ConditionList
from main.models import *
import utils
from datetime import datetime

from django.template import Template, Context
from django.core.mail import send_mail

EMAIL_CONFIRM_FROM = 'Beatwrit<confirm@beatwrit.com>'
EMAIL_CONFIRM_SUBJECT = 'Email Confirmation'
email_body = """{{ bwuser.authuser.username }}

Confirmation of your email address is almost complete.  Please visit the url below to let us know that this is indeed your email address.

{{ url|safe }}

Peace,
Beatwrit
"""

class EmailChangeManager(object):
    token = None
    email = None

    @classmethod
    def begin_change(cls, bwuser, new_email, domain_str=None, params=''):
        EmailChangeToken.objects.filter(bwuser__pk=bwuser.pk).delete()
        
        t = EmailChangeToken()
        t.bwuser = bwuser
        t.email = new_email
        t.token = utils.random_positive_long()
        
        if params and params[0] != '&':
            params = '&' + params
        domain_str = beatwrit.settings.DOMAIN_STR
        h = create_hash(bwuser.id, t.token)
        url = 'http://%s/authors/%s/econf?h=%s%s' % (domain_str,bwuser.id, h, params)
        body = Template(email_body).render(Context ({ 'url': url, 'bwuser':bwuser })) 
        try:
            send_mail(EMAIL_CONFIRM_SUBJECT, body, EMAIL_CONFIRM_FROM, [new_email], fail_silently=False)
        except:
            return ConditionList.FAIL
        
        t.save()
        return ConditionList.SUCCESS

    def token_exists(self, h, bwuid):
        h, bwuid = (long(h), long(bwuid))
        _token = create_hash(h, bwuid)
        
        try:
            self.token  = EmailChangeToken.objects.get(token=_token)
            self.email = self.token.email
        except:
            return ConditionList.EMAIL_CHANGE_FAIL
        
        if datetime.now() > self.token.expiration:
            print "Email change token expired"
            return ConditionList.EMAIL_CHANGE_FAIL
        print (self.token.bwuser.pk, bwuid)
        if self.token.bwuser.pk != bwuid:
            print "Email change token invalid: token.bwuid and bwuid don't match."
            return ConditionList.EMAIL_CHANGE_FAIL
        return ConditionList.EMAIL_CHANGE_SUCCESS

    def finalize_change(self, bwuser):
        authu = bwuser.authuser
        authu.email = self.token.email
        print 'Changing the email address of %s to "%s"' % (str(bwuser), self.token.email)
        authu.save()
        self.token.delete()
        return authu.email

def create_hash(num1, num2):
    r = long(num1) ^ long(num2)
    if num1 > 0 and num2 > 0 and r > 0:
        return r 
    else:
        raise Exception("Invalid numbers to create hash (probably too large): num1=%s, num2=%s, result=%s" % (num1, num2, r))


