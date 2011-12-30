from facebookapps.linedrop.models import *
from django.contrib import admin

class FacebookUserAdmin(admin.ModelAdmin):
    fields = ['facebookid','name', 'receivedinvites', 'careermedals', 'availmedals']

class LitletAdmin(admin.ModelAdmin):
    fields = ['creator', 'coauthor', 'ordering', 'options', 'enddate']

class LineAdmin(admin.ModelAdmin):
    fields = ['author', 'date', 'content'] 


admin.site.register(Litlet, LitletAdmin)
#admin.site.register(Litlet)
admin.site.register(FacebookUser, FacebookUserAdmin)
#admin.site.register(FacebookUser)
admin.site.register(Line)
admin.site.register(Medal)
admin.site.register(Invite)


"""

    writtype = models.CharField(max_length=20, default=_default, help_text=ht)
    max_words_per_contribution = models.IntegerField(help_text=ht, default=_default)
    joining_period_days = models.IntegerField(help_text=ht, default=_default)
    max_turn_length_days = models.IntegerField(help_text=ht, default=_default)
    blurb_plot_summary = models.TextField(help_text=ht, default=_default)
    can_join_in_progress = models.BooleanField(help_text=ht, default=_default)
    is_invite_only = models.BooleanField(help_text=ht, default=_default)
    allow_rtf_formatting = models.BooleanField(help_text=ht, default=_default)
"""
