from main.models import *

"""
    user
    profile_visibility = enum_ex(
                                    (0, 'FULL_PUBLIC', 'Anyone can browse the list of your writs.', 'Public'), 
                                    (1, 'ONLY_CIRCLE', 'Only users in your circle can browse your list of writs.', 'Only Circle'), 
                                    (2, 'ONLY_AUTHOR', 'Only you can browse your list of writs.', 'Private'))
    
    public_visibility = enum_ex(
                                (0, 'FRIENDS','Only those in the circle of the authors can see the writ.','circle'),
                                (1, 'ONLY_AUTHORS', 'Only the authors can see the writ.','authors'),
                                (2, 'FULL_PUBLIC', 'The writ is viewable by anyone.','public'))
"""

class AccessModel():
    @staticmethod
    def can_access_writ(context_bwuser, writ):
        if writ.settings.public_visibility == WritSettingsChoices.public_visibility.FULL_PUBLIC:
            return True
        if context_bwuser == None:
            return False
       
        if writ.settings.public_visibility == WritSettingsChoices.public_visibility.ONLY_AUTHORS:
            return Writ.objects.filter(participants__=context_bwuser).exists()
        elif writ.settings.public_visibility == WritSettingsChoices.public_visibility.FRIENDS:
            return Writ.objects.filter(participants__circle=context_bwuser).exists()
        else:
            raise Exception("Not implemented")
            
    @staticmethod
    def can_access_profile(context_bwuser, bwuser):
        if context_bwuser == None:
            if bwuser.profile_visibility == BeatwritUserChoices.profile_visibility.FULL_PUBLIC:
                return True
            else:
                return False
        if context_bwuser.id == bwuser.id:
            return True
        if bwuser.profile_visibility == BeatwritUserChoices.profile_visibility.FULL_PUBLIC:
            return True
        elif bwuser.profile_visibility == BeatwritUserChoices.profile_visibility.FRIENDS:
            return bwuser.is_in_circle(context_bwuser)
        elif bwuser.profile_visibility == BeatwritUserChoices.profile_visibility.ONLY_AUTHOR:
            return False
        else:
            raise Exception("Not implemented")

    @staticmethod
    def can_access_addition(context_bwuser, addition):
        return AccessModel.can_access_writ(context_bwuser, addition.writ)

