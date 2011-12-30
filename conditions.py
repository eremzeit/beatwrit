import pdb

condition_init = (
    ('SUCCESS','Whatever you did was a success!', True),
    ('FAIL',"Whatever you tried to do, didn't work.", False),
 
    ('LOGIN_FAIL__INVALID_CREDENTIALS',"The username and password didn't match what we've got.", False),
    ('LOGIN_FAIL__ACCOUNT_DISABLED',"For whatever reason, this account has been disabled.", False),

    ('NO_POST__TOO_MANY_WORDS','Cannot make a new addition.  There were too many words in your post.', False),
    ('NO_POST__WRIT_HAS_ENDED','Cannot make a new addition.  The writ has ended.', False),
    ('NO_POST__NOT_USERS_TURN',"Cannot make a new addition.  The turn type is set to round-robin and it isn't your turn to contribute.", False),
    
    ('WRIT_VIEW_PERM__ONLY_AUTHORS',"This writ can only be viewed by the authors.", False),
    ('WRIT_VIEW_PERM__ONLY_CIRCLE',"This writ can only be viewed by those in at least one of the authors' circle.", False),
   
    ('JOIN_FAIL__ALREADY_JOINED','You are already a member of this writ.', False),
    ('CANT_JOIN__ONLY_CIRCLE', "This writ can be only joined by people in the circle the authors.", False),
    ('CANT_JOIN__INVITE_ONLY', "Joining this writ is invite-only.  Check out the list of joinable writs <a>here</a>", False),
    ('CAN_JOIN', "", True),
    ('CANT_JOIN', "Looks like there was a problem joining the writ.  Perhaps try again one more time.", False),
    
    ('ADD_TO_CIRCLE_SUCCESS', "The author has been added to your circle.", True),
    ('ADD_TO_CIRCLE_FAIL', "Can't add author to circle.", False),
    ('ADD_TO_CIRCLE_FAIL__ALREADY_IN_CIRCLE', "Can't add author to circle because this author is already in your circle.", False),
    
    ('REMOVE_FROM_CIRCLE_SUCCESS', "The author has been removed from your circle.", True),
    ('REMOVE_FROM_CIRCLE_FAIL', "Couldn't remove author from circle.", False),

    ('NOD_FAIL__NO_NODS_TO_GIVE', "You do not have enough nods remaining to give this nod.  You can earn more nods to give by making contributions to writs or by receiving nods.", False),
    ('NOD_FAIL__CANT_NOD_TO_SELF', "Can't give a nod to onesself", False),
    ('NOD_FAIL', "You are unable to give a nod for this contribution.", False),
    ('NOD_SUCCESS', "You have successfuly given a nod.", True),
    
    ('EMAIL_CHANGE_FAIL', "Your email could not be changed.", False),
    ('EMAIL_CHANGE_SUCCESS', "Your email has been changed successfully.", True),

    ('JOIN_SUCCESS__ROUND_ROBIN', "You are now a member of this writ and it's your turn to contribute.", True),
    ('JOIN_SUCCESS__FFA', "You are now a member of this writ.  You may contribute at any time.", True),
    
    ('NOD_SUCCESS',"Your nod has been given.", True),
    ('NOD_UNSUCCESS__ALREADY_NODDED',"Oops, looks like you already gave a nod to this particular addition.", False),
    ('NOD_UNSUCCESS__NOT_ENOUGH_NODS',"Oops, looks like you don't have enough nods.", False),

    ('LOGIN_FAIL__INVALID_USERNAME', "Invalid username", False),

    ('404_ERROR',"Oops! We had a problem providing what you were looking for.  Try clicking your browser's back button and trying again.  If that doesn't work, try sending an email to <a href='mailto:erem.gumas@gmail.com'>erem.gumas@gmail.com</a>.", False),

    ('WRIT_NOT_FOUND', "We can't seem to find the writ you are looking for.", False),
)

#make condition strings for:
#published_to_beatwrit = "You have successfully published to the beatwrit."

class Condition(object):
    def __init__(self, name, message,value):
        self.name = name
        self.value = value
        self.message = message

    def __eq__(self, other):
        if isinstance(other, Condition):
            if self.value == other.value:
                return True
            return False
        else:
            return NotImplemented
    def issuccess(self):
        if isinstance(self, ConditionSuccess):
            return True
        else:
            return False

class ConditionSuccess(Condition):
    pass

class ConditionFail(Condition):
    pass

class _ConditionList(object):
    d = {}
    l = []
    for i in xrange(len(condition_init)):
        c = condition_init[i]
        cond = None
        if c[2]:
            cond = ConditionSuccess(c[0], c[1], i)
        else:
            cond = ConditionFail(c[0], c[1], i)
        d[cond.name] = cond
        l.append(cond)
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.l[key]
        return NotImplemented

    def __getattr__(self, name):
        if not name in self.d:
            raise Exception("Name %s not found in ConditionList" % name)
        return self.d[name] 
ConditionList = _ConditionList()

#print ConditionList.CAN_JOIN.message
#print ConditionList[3].message
