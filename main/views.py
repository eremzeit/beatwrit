from utils import *
from conditions import ConditionList as ConditionList
from main.models import *
from main.forms import *
import main.strings
from main.oftheday import WordOfTheDay
from main.pagecontexts import WritViewPageContext, MyBeatwritPageContext, LandingPageContext, BrowseWritsTable
from main.userutils import EmailChangeManager


from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import simplejson as json

from urlparse import urlparse
import datetime
import pdb

def home(request):
    if not request.user.is_authenticated():
        lp_context = LandingPageContext(request)
        return render_to_response("landing.html", {'lp_context':lp_context}, context_instance=RequestContext(request))
    else:
        return author(request, bwuser=request.user.beatwrituser)

def browse(request):
    print 'request.GET dict: %s' % request.GET
    table = BrowseWritsTable(request.GET)
    return render_to_response('browse.html', {'writtable':table}, context_instance=RequestContext(request))

def joinbrowse(request):
    gets = {}
    gets.update(request.GET)
    gets.update({'joinable':'1'})
    table = BrowseWritsTable(gets)
    return render_to_response("joinbrowse.html", {'writtable': table}, context_instance=RequestContext(request))

@login_required
def author(request, bwuid=None, bwuser=None):
    if bwuid:
        bwuid = int(bwuid)
        if not bwuser:
            bwuser = BeatwritUser.objects.get(id=bwuid)
    if not bwuid or bwuid == request.user.beatwrituser.pk:
        return _mybeatwritpage(request, bwuser)
    else:
        return _theirbeatwritpage(request,bwuser)

def _mybeatwritpage(request, bwuser):
    mbw_context = MyBeatwritPageContext(bwuser) 
    return render_to_response("mybeatwrits.html", {'mbw_context':mbw_context, }, context_instance=RequestContext(request))

def _theirbeatwritpage(request, bwuser):
    mbw_context = MyBeatwritPageContext(bwuser) 
    return render_to_response("theirbeatwrits.html", {'mbw_context':mbw_context, }, context_instance=RequestContext(request))
    

def myprofile(request):
    if not request.user.is_authenticated():
        return oops(request)
    return author(request, bwuid=request.user.beatwrituser.pk)

@login_required
def writjoin(request, writid=None):
    writ = None
    try:
        writ = Writ.objects.get(id=writid)
    except:
        messages.error(request, ConditionList.WRIT_NOT_FOUND.message)
        return HttpResponseRedirect('/')
    
    bwuser = request.user.beatwrituser
    c = writ.can_join(bwuser)
    if c.issuccess():
        cond_res = writ.add_participant(bwuser)
        if cond_res.issuccess():
            if writ.settings.turn_type == writ.settings.choices.turn_type.ROUND_ROBIN:
                messages.info(request, ConditionList.JOIN_SUCCESS__ROUND_ROBIN.message)
                return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST
            elif writ.settings.turn_type == writ.settings.choices.turn_type.FREE_FOR_ALL:
                messages.info(request, ConditionList.JOIN_SUCCESS__FREE_FOR_ALL.message)
                return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST
        else: #fail
            messages.error(request, cond_res.message)
            return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST
        messages.info(request, c.value) 
        return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST

    elif (c == ConditionList.CANT_JOIN__ONLY_CIRCLE):
        messages.info(request, ConditionList.CANT_JOIN__ONLY_CIRCLE.message)
        return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST
    elif (c == ConditionList.CANT_JOIN__INVITE_ONLY):
        messages.info(request, ConditionList.CANT_JOIN__INVITE_ONLY.message)
        return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST
    else:    
        messages.info(request, c.message)
        return HttpResponseRedirect('/writs/%s' % writid) # Redirect after POST


@login_required
@require_http_methods(['GET'])
def addcircle(request, bwuid=None):
    try:
        bwuser_to_add = BeatwritUser.objects.get(pk=bwuid)
    except:
        if 'next' in request.GET:
            messages.info(request, ConditionList.FAIL.value)
            return HttpResponseRedirect('%s' % request.GET['next'])
        else:
            messages.info(request, ConditionList.FAIL.value)
            return HttpResponseRedirect('/')
    
    if request.user.is_authenticated():
        bwuser = request.user.beatwrituser
        c = bwuser.can_add_to_circle(bwuser_to_add)
        if c.issuccess():
            bwuser.add_to_circle(bwuser_to_add)
            if 'next' in request.GET:
                messages.info(request, c.message)
                return HttpResponseRedirect('%s' % request.GET['next'])
            else:
                messages.info(request, c.message)
                return HttpResponseRedirect('/')

        else:
            if 'next' in request.GET:
                messages.info(request, c.message)
                return HttpResponseRedirect('%s' % request.GET['next'])
            else:
                messages.info(request, c.message)
                return HttpResponseRedirect('/')

    else:
        return oops(request, message="You must be logged in to add someone to your circle.")
    
@login_required
@require_http_methods(['GET'])
def removecircle(request, bwuid=None):
    try:
        bwuser_to_rem = BeatwritUser.objects.get(pk=bwuid)
    except:
        if 'next' in request.GET:
            messages.error(request, ConditionList.REMOVE_FROM_CIRCLE_FAIL.value)
            return HttpResponseRedirect('/' if 'next' in request.GET else '%s' % request.GET['next'])
    
    bwuser = request.user.beatwrituser
    bwuser.circle.remove(bwuser_to_rem)
    if 'next' in request.GET:
        messages.error(request, ConditionList.REMOVE_FROM_CIRCLE_SUCCESS.message)
        return HttpResponseRedirect('/' if 'next' in request.GET else '%s' % request.GET['next'])

def usercreate(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST) 
        if form.is_valid():
            error = False
            if form.is_username_taken() or form.is_username_invalid() or form.are_passwords_invalid():
                error = True 
            if not error: 
                bwu = form.make_user()
                user = authenticate(username=bwu.authuser.username, password=form.cleaned_data['password1'])
                r = EmailChangeManager.begin_change(bwu, form.cleaned_data['email'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/profile')
                    else:
                        return oops(request)
                else:
                    return oops(request)
                return HttpResponseRedirect('/authors/%s' % u.pk) # Redirect after POST
            else:
                return render_to_response('newuser.html', {'form': form, }, context_instance=RequestContext(request)) 
    else:
        if request.user.is_authenticated():
            django.contrib.auth.logout(request)
        form = NewUserForm() # An unbound form
    return render_to_response('newuser.html', {'form': form, }, context_instance=RequestContext(request)) 

@login_required
def usersettings(request, bwuid=None):
    bwuid = long(bwuid)
    bwuser = request.user.beatwrituser
    if bwuid != bwuser.pk:
        return Http404()
    if request.method == 'GET':
        emailform, passform, optionsform = default_settings_forms(bwuser)
        return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform}, context_instance=RequestContext(request)) 
    
    if request.method == 'POST':
        if 'form_email' in request.POST:
            return changeemail(request, bwuser=bwuser)
        if 'form_options' in request.POST:
            return changeoptions(request, bwuser=bwuser)
        if 'form_password' in request.POST:
            return changepassword(request, bwuser=bwuser)

def default_settings_forms(bwuser):
    return (EmailChangeForm.default(bwuser), PasswordChangeForm.default(bwuser), OptionsChangeForm.default(bwuser))

def changeemail(request, bwuid=None, bwuser=None):
    if not bwuser:
        bwuser = BeatwritUser.objects.get(pk=bwuid)
    
    emailform = EmailChangeForm(request.POST)
    if emailform.is_valid():
        #begin emailing process
        r = EmailChangeManager.begin_change(bwuser, emailform.cleaned_data['emailaddress'], params='settings=1')
        if r.issuccess():
            return message(request, header="More more step...", message="We have sent a confirmation email you the email address you gave.  Please click the link in the email to confirm that the email address is yours.")
        else:
            emsg = "We had a problem when trying to send a confirmation email.  Try reentering the email address and submitting again."
            dummy, passform, optionsform = default_settings_forms(bwuser)
            return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform, 'email_error_message': emsg}, context_instance=RequestContext(request)) 
    else:
        #recreate other unbound forms
        pwform = PasswordChangeForm() 
        sform = OptionsForm()
        return render_to_response('settings.html', {'optionsform': sform, 'emailform':eform, 'passform':pwform}, context_instance=RequestContext(request)) 

#@require_http_methods(['POST'])
def emailconfirm(request, bwuid):
    h = None
    if 'h' in request.GET:
        h = request.GET['h']
    else:
        return debug_or_404(request, message="The proper parameters were not found.  Expecting 'h' parameter")
    manager = EmailChangeManager()
    if manager.token_exists(h, bwuid).issuccess():
        if request.user.is_authenticated():
            #then we can assume the user is legit
            new_email = manager.finalize_change(request.user.beatwrituser)
            
            bwuser = request.user.beatwrituser
            if 'settings' in request.GET:
                settings = request.GET['settings']
                emailform, passform, optionsform = default_settings_forms(bwuser)
                emsg = "Email successfully changed"
                return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform, 'email_success_msg':emsg}, context_instance=RequestContext(request)) 
            else:
                pdb.set_trace()
                header = "Email was successfully set to %s" % new_email
                msg = "<p>You can change you the settings for receiving email by visiting the <a href='/%s/settings'>accounts settings</a> page.</p><p>Would you like to visit your <a href='%s'>beatwrits page</a>, or perhaps <a href='/joinbrowse'>browse the joinable writs</a>?</p>" % (bwuser.id, bwuser.get_absolute_url())
                return message(request, message=msg, header=header)

        else:
            #ask the user to give password first to confirm that this person is truly the user.
            #ie. take the user to another page where they enter their pass and POST back to the same page.
            return message(request, message="Need to enter pass")
    return oops(request)


@login_required
@require_http_methods(['POST'])
def changepassword(request, bwuid=None, bwuser=None):
    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        d = form.cleaned_data
        user = request.user
        if not user.check_password(d['password']):
            return message(request, message="Your password could not be changed because the given password did not match the one we have listed for your account.")
        if d['password1'] == d['password2']:
            user.set_password(form.cleaned_data['password1'])
            user.save()
            password_success = "Password successfully changed"
            emailform, passform, optionsform = default_settings_forms(bwuser)
            return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform, 'password_success':password_success}, context_instance=RequestContext(request)) 
        else:
            return message(request, message="Your password could not be changed because the given passwords do not match.")
    else:
        return message(request, message="Your password has been successfully changed")

@login_required
@require_http_methods(['POST'])
def changeoptions(request, bwuid=None, bwuser=None):
    if not bwuser:
        bwuser = BeatwritUser.objects.get(pk=bwuid)
    optionsform = OptionsChangeForm(request.POST)
    if optionsform.is_valid():
        optionsform.save_settings(bwuser)
        emailform, passform, optionsform = default_settings_forms(bwuser)
        options_changed = "Your settings have been successfully changed."
        return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform, 'options_changed':options_changed }, context_instance=RequestContext(request)) 
    else:
        dummy, passform, optionsform = default_settings_forms(bwuser)
        return render_to_response('settings.html', {'optionsform': optionsform, 'emailform':emailform, 'passform':passform, 'password_success':password_success}, context_instance=RequestContext(request)) 

     
@login_required
def writcreate(request):
    if request.method == 'POST':
        form = NewWritForm(request.POST) 
        if form.is_valid():
            w = form.make_writ(request.user.beatwrituser) 
            return HttpResponseRedirect('/writs/%s' % w.pk) # Redirect after POST
    else:
        form = NewWritForm() # An unbound form

    return render_to_response('newwrit.html', {'form': form, }, context_instance=RequestContext(request)) 
    
def writdelete(request, writid=None):
    if request.user.is_superuser:
        writ = get_object_or_404(Writ, pk=writid) 
        writ.delete()
        return HttpResponseRedirect('/authors/%s' % request.user.beatwrituser.pk) # Redirect after POST

def writview(request, writid=None):
    if request.method == 'GET':
        writ = get_object_or_404(Writ, pk=writid) 
        writ.update_state()

        message = None
        bwuser = None
        if not request.user.is_anonymous():
            bwuser = request.user.beatwrituser 
            if 'action' in request.GET:
                if request.GET['action'] == 'nod':
                    addition_id = int(request.GET['addition'])
                    addition = Addition.objects.get(pk=addition_id)
                    cond = addition.make_nod(bwuser)
                    if cond.issuccess():
                        messages.success(request, main.strings.nod_given_successfully_msg)
                    else:
                        messages.error(request, cond.message)
                    return HttpResponseRedirect(request.path)
            if not writ.can_view(bwuser):
                if writ.settings.public_visibility == WritSettingsChoices.public_visibility.FRIENDS:
                    return oops(request, title="Can't view writ", message=ConditionList.WRIT_VIEW_PERM__ONLY_CIRCLE.message)
                elif writ.settings.public_visibility == WritSettingsChoices.public_visibility.ONLY_AUTHORS:
                    return oops(request, title="Can't view writ", message=ConditionList.WRIT_VIEW_PERM__ONLY_AUTHORS.message)
        else:
            bwuser = None
            if writ.settings.public_visibility == WritSettingsChoices.public_visibility.FRIENDS:
                return oops(request, title="Can't view writ", message=ConditionList.WRIT_VIEW_PERM__ONLY_CIRCLE.message)
            elif writ.settings.public_visibility == WritSettingsChoices.public_visibility.ONLY_AUTHORS:
                return oops(request, title="Can't view writ", message=ConditionList.WRIT_VIEW_PERM__ONLY_AUTHORS.message)
       
        writ.increment_viewcount()
        wvc = WritViewPageContext(request, writ)
        wordoftheday = WordOfTheDay()
        writ.check_is_finished()
        d = {   'writ': writ, 
                'request': request, 
                'wvc': wvc,
                'wordoftheday': wordoftheday,
                'message' : message,
                }
        return render_to_response("beatview.html", d, context_instance=RequestContext(request))
    elif request.method == 'POST':
        return oops(request)

def writpost(request):
    if request.method == 'GET':
        return oops(request)
    elif request.method == 'POST':
        writid = request.POST['writid']
        if not writid:
            raise Exception("Writid not embedded correctly.")
        writ = get_object_or_404(Writ, pk=writid) 
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next=%s' % request.path)
        
        content = request.POST['additiontext']
        if writ.validate_addition(request.user.beatwrituser,content):
            #infos = writ.get_participant_infos()
            writ.add_addition(request.user.beatwrituser,content)
            
            #msg = published_to_beatwrit
            return HttpResponseRedirect('/writs/%s' % str(writid))
        else:
            return oops(request, message=not_your_turn)

def loginview(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        if 'keepsignedin' in request.POST:
            keepsignedin = request.POST['keepsignedin']
        else:
            keepsignedin = None
        if not (username and password):
           #return render_to_response("landing.html", d, context_instance=RequestContext(request))
            messages.error(request, ConditionList.LOGIN_FAIL__INVALID_CREDENTIALS.message)
            return HttpResponseRedirect('/login')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if keepsignedin:
                    request.session.set_expiry(604800) #two weeks
                else:
                    request.session.set_expiry(0) #when the browser closes
                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect('/authors/%s' % user.beatwrituser.id)
            else:
                messages.error(request, ConditionList.LOGIN_FAIL__ACCOUNT_DISABLED.message)
                return HttpResponseRedirect('/login')
        else:
            messages.error(request, ConditionList.LOGIN_FAIL__INVALID_CREDENTIALS.message) 
            return HttpResponseRedirect('/login')
    elif request.method == 'GET':
        #return oops(request, 'aoeu')
        d = {}
        if 'next' in request.GET:
            d['next'] = request.GET['next']
        return render_to_response("login.html", d,context_instance=RequestContext(request))

def autologin(request, uid, token_no):
    if not token_no:
        return Http404 
    user = authenticate(user_id=long(uid), token_no=long(token_no))
    if user and user.is_active:
        login(request, user) 
        if 'next' in request.GET:
            url = urlparse(request.GET['next']).geturl()
            if url != '':
                return HttpResponseRedirect(url)
        return HttpResponseRedirect('/')
    else:
        return Http404



def logout(request):
    django.contrib.auth.logout(request)

#---------------------------------
#----------ERROR----------------
#---------------------------------

def message (request, message=None, header=None):
    if not message:
        message = "Not sure why"
    if not header:
        header = "---"
    return render_to_response('message.html', {'body':message, 'header':header}, context_instance=RequestContext(request)) 

#def message (request, message=None):
#    if not message:
#        message = "Not sure why"
#    return render_to_response('mainwrap.html', {'message':message, 'header':header}, context_instance=RequestContext(request)) 
    
def debug_or_404(request, message=None):
    if beatwrit.settings.DEBUG:
        return message(request, message)
    else:
        return Http404

def oops(request, message=None, title=None):
    if not message:
        message = main.strings.default_error
    if not title:
        title = "This page cannot be viewed."
    return render_to_response('oops.html', {'message':message, 'header':title}, context_instance=RequestContext(request)) 

#---------------------------------
#----------TESTING----------------
#---------------------------------
def authorsfriendstest(request, bwuid=None, bwuser=None):
    if not bwuser:
        bwuser = BeatwritUser.objects.get(pk=bwuid)

    friends = bwuser.friends.all()
    innerHTML = ''
    for friend in friends:
        innerHTML = innerHTML + '<p><a href="/authors/%s">%s</a></p>' % (friend.pk, friend)

    return render_to_response("mainwrap.html", {'content': innerHTML}, context_instance=RequestContext(request))

def _autologin(request, writ):
    django.contrib.auth.logout(request)
    up_username = writ.get_user_order()[0].authuser.username
    user = authenticate(username=up_username, password=up_username)
    if user is not None:
        if user.is_active:
            login(request, user)
    return user


def writview_autologin(request, writid=None):
    writ = get_object_or_404(Writ, pk=writid)
    user = _autologin(request, writ)
    if user is not None:
        if user.is_active:
            return HttpResponseRedirect('/writs/%s' % writid)
        else:
            return oops(request)
    else:
            return oops(request)

def writview_autologinpost(request, writid=None):
    writ = get_object_or_404(Writ, pk=writid)
    user = _autologin(request, writ)
     
    if user is not None:
        if user.is_active:
            content = utils.truncate_words(rand_sentence(), writ.settings.max_words_per_contribution)
            writ.add_addition(request.user.beatwrituser,content)
            return HttpResponseRedirect('/writs/%s' % str(writid))
        else:
            return oops(request)
    else:
            return oops(request)
    
def writuserordertest(request,writid=None):
    if not writid:
        return oops(request)
    else:
        writ = get_object_or_404(Writ, pk=writid)
        parts = writ.get_user_order()
        innerhtml = ''
        for part in parts:
            innerhtml = innerhtml + '<p>' + part.authuser.username + '</p>'
        return render_to_response("mainwrap.html", {'content': innerhtml}, context_instance=RequestContext(request))

def writbrowse(request):
    writs = Writ.objects.all()
    
    innerhtml = ''
    for writ in writs:
        innerhtml = innerhtml + '<a href="/writs/%s">%s</a>\n' % (writ.id, writ.id)
    return render_to_response("mainwrap.html", {'content': innerhtml}, context_instance=RequestContext(request))


def writadditionstest(request, writid=None):
    if not writid:
        return oops(request)
    
    writ = get_object_or_404(Writ, pk=writid)
    additions = writ.addition_set.order_by('-position').all()

    innerhtml = ''
    for addition in additions:
        row = '<tr><td>%s</td>' % addition.author
        row = row + '<td>%s</td>' % addition.position
        row = row + '<td>%s</td>' % addition.date
        row = row + '<td>%s</td>' % addition.content
        row = row + '</tr>'
        innerhtml = innerhtml + row

    innerhtml = '<table>%s</table>' % innerhtml
    return render_to_response("mainwrap.html", {'content': innerhtml}, context_instance=RequestContext(request))

def writsettingstest(request, writid=None):
    if not writid:
        return oops(request)
    
    writ = get_object_or_404(Writ, pk=writid)
    headers = '''
    '''
        
    row = '<tr>'
    row = row + '<td>max_words_per_contribution</td>' 
    row = row + '<td>%s</td>' % writ.settings.max_words_per_contribution 
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>turn_length</td>'     
    row = row + '<td>%s</td>' % utils.minutes_to_natural(writ.settings.turn_length, simple=True)
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>who_can_join</td>'
    row = row + '<td>%s</td>' % writ.settings.who_can_join
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>endingtype</td>'     
    row = row + '<td>%s</td>' % writ.settings.endingtype
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>wordlimit</td>'     
    row = row + '<td>%s</td>' % writ.settings.wordlimit
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>inactive_time</td>'     
    row = row + '<td>%s</td>' % writ.settings.inactive_time
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>endingdate</td>'     
    row = row + '<td>%s</td>' % writ.settings.endingdate
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>public_visibility</td>'     
    row = row + '<td>%s</td>' % writ.settings.public_visibility
    row = row + '</tr>'

    row = row + '<tr>'
    row = row + '<td>turntype</td>'
    row = row + '<td>%s</td>' % writ.settings.turntype
    row = row + '</tr>'

    innerhtml = '<table>%s \n %s</table>' % (headers, row)
    return render_to_response("mainwrap.html", {'content': innerhtml}, context_instance=RequestContext(request))


def nodsquery(request):
    nods = Nod.objects.all()
    if 'receiver' in request.GET:
        bwuid = request.GET['receiver'] 
        nods = nods.filter(receiver__id=bwuid)
    if 'writid' in request.GET:
        writid = request.GET['writid']
        adds = Addition.objects.filter(writ__id=writid)
        nods = nods.filter(addition__in=adds)
    s = u'Results: ' + unicode(nods)
    return render_to_response("mainwrap.html", {'content': s}, context_instance=RequestContext(request))
    
