from django.conf import settings

import pdb

from django.contrib.auth.models import User
import utils


class TokenAuthenticationBackend:
    def authenticate(self, user_id=None, token_no=None):
        if not user_id and token_no:
            return None
        res = TokenManager.check_token(user_id, token_no)
        if res:
            return User.objects.get(pk=user_id)
        else:
            print 'Token not found'
            return None
            
    def get_user(self, user_id=None):
        return User.objects.get(pk=user_id)
        
class TokenManager:
    @classmethod 
    def make_autologin_token(cls, user):
        from main.models import LoginToken
        LoginToken.objects.filter(user__id=user.pk).delete()
        t = LoginToken()
        t.user = user
        t.expiration = utils.week_from_now()
        t.save()
        return t
    
    @classmethod 
    def check_token(cls, uid, token_no):
        from main.models import LoginToken
        tokens = LoginToken.objects.filter(token=token_no)
        if len(tokens) == 0:
            return False
        elif len(tokens) == 1:
            t = tokens[0]
            if t.user_id == uid:
                tokens.delete()
                return True
            else:
                return False
        else:
            raise Exception("Multiple tokens found.")

    @classmethod 
    def make_autologin_url(cls, user, next_url=''):
        t = TokenManager.make_autologin_token(user)
        url = 'http://%s/_l/%s/%s' % (settings.DOMAIN_STR, user.id, t.token)
        if next_url:
            url = url + '?next=' + next_url
        return url



def test_token():
    user = User.objects.get(id=8)
    url = TokenManager.make_autologin_url(user, next_url='/')
    
    print LoginToken.objects.all()[:]
    print url

