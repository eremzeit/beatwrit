import sys
import beatwrit.settings

from conditions import ConditionList as ConditionList
from main.models import *
import utils
from datetime import datetime




class UserContext(object):
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.bwuser = self.user.bwuser

    def get_active_writs(self):
        pass
