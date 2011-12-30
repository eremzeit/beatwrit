import utils
from conditions import ConditionList as ConditionList
from main.models import *
from main.forms import *
import main.strings
from main.oftheday import WordOfTheDay
from main.pagecontexts import WritViewPageContext, MyBeatwritPageContext, LandingPageContext, BrowseWritsTable
from main.userutils import EmailChangeManager
import main.jsonmodels
from main.fetching import WritsSurface, WritsAccessor

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

#HttpRequest.is_ajax()



###################
####   JSON     ###
###################
get_writs_legal_params = {
                    'p':(r'[\d]{1,2}', '0'), 
                    'ps':(r'[\d]{1,500}', '10'), 
                    'ord': (r'date','date'),
                    }

#   URL scheme:     /authors/8/activewrits_?p=0, ps=100
#    
#   ~~params~~
#   p               page
#   ps              page size
#   ord             ordering scheme (defaults to date)
@require_http_methods(['GET'])
@login_required
def active_writs(request, bwuid):
    params = utils.ParameterCleaner.clean(get_writs_legal_params, request.GET)
    bwuser = BeatwritUser.objects.get(id=bwuid)
    w = WritsAccessor(request.user.beatwrituser).users_active_by_date(bwuser, pagenum=params['p'], pagesize=params['ps'])[:]
    w = main.jsonmodels.BeatwritJSON.json_all(w)
    return HttpResponse(w, mimetype="application/json")
    

#   URL scheme:     /authors/8/compwrits_?p=0, ps=100
#    
#   ~~params~~
#   p               page
#   ps              page size
#   ord             ordering scheme (defaults to date)

@require_http_methods(['GET'])
@login_required
def completed_writs(request, bwuid):
    params = utils.ParameterCleaner.clean(get_writs_legal_params, request.GET)
    bwuser = BeatwritUser.objects.get(id=bwuid)
    w = WritsAccessor(request.user.beatwrituser).users_completed_by_date(bwuser, pagenum=params['p'], pagesize=params['ps'])
    w = main.jsonmodels.BeatwritJSON.json_all(w)
    return HttpResponse(w, mimetype="application/json")



#   URL scheme:     /authors/8/circwrits_?p=0, ps=100
#    
#   ~~params~~
#   p               page
#   ps              page size
#   ord             ordering scheme (defaults to date)
@require_http_methods(['GET'])
@login_required
def circle_writs(request, bwuid):
    params = utils.ParameterCleaner.clean(get_writs_legal_params, request.GET)
    bwuser = BeatwritUser.objects.get(id=bwuid)
    w = WritsAccessor(request.user.beatwrituser).users_circle_by_date(bwuser, pagenum=params['p'], pagesize=params['ps'])
    w = main.jsonmodels.BeatwritJSON.json_all(w)
    return HttpResponse(w, mimetype="application/json")


#   URL scheme:     /authors/8/commwrits_?p=0, ps=100
#    
#   ~~params~~
#   p               page
#   ps              page size
#   ord             ordering scheme (defaults to date)
@require_http_methods(['GET'])
@login_required
def community_writs(request, bwuid):
    params = utils.ParameterCleaner.clean(get_writs_legal_params, request.GET)
    bwuser = BeatwritUser.objects.get(id=bwuid)
    w = WritsAccessor.community_by_date(bwuser, pagenum=params['p'], pagesize=params['ps'])
    w = main.jsonmodels.BeatwritJSON.json_all(w)
    return HttpResponse(w, mimetype="application/json")

