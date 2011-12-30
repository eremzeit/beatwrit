#
#   jsonmodels.py
#
#   Contains functions for converting django model objects into json objects fit for consumption.

from types import *
from datetime import datetime
import utils
from django.utils import simplejson as djangojson

class BeatwritJSON(object):
    from main.models import *
    @staticmethod
    def pack(obj):
        jsonobj = {}
        for var, val in obj.__dict__.items():
            if type(val) is InstanceType:
                if type(val) is BeatwritUser:
                    jsonobj[var+'_url'] = val.get_absolute_url()
            elif type(val) is type(datetime):
                jsonobj['_rel__' + var] = utils.timedelta_to_natural(datetime.now() - self.date, simple=True)
            elif type(val) in [NoneType, BooleanType, IntType, LongType, FloatType, StringType, UnicodeType]:
                jsonobj[var] = val
        return jsonobj
    
    @staticmethod
    def json(obj):
        if not type(obj) is InstanceType:
            raise Exception("Expecting InstanceType.  Got %s" % str(type(obj)))
        return djangojson.dumps(BeatwritJSON.pack(obj))
    
    @staticmethod
    def pack_all(obj_list): 
        out = []
        for i in xrange(len(obj_list)):
            print 'processing item of type %s' % str(type(obj_list[i]))
            out.append(BeatwritJSON.pack(obj_list[i]))
        return out

    @staticmethod
    def json_all(obj_list):
        return djangojson.dumps(BeatwritJSON.pack_all(obj_list))





        
         
    
