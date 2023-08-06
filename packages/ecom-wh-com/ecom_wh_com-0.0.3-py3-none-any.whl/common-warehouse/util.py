import json,datetime
import copy,uuid,os
from ecomshared.helpers import Encoder,get_source


def create_event( detail_type:str,detail:dict,EVENT_BUS_NAME) ->  dict:
  
    """ create Event Bridge event from input """
    event_bridge_event = {
        "Time" : datetime.datetime.now(),
        "Source" : "ecommerce.warehouse.validate",
        "Resources" : [],
        "DetailType" : detail_type,
        "Detail" : json.dumps(detail,cls=Encoder),
        "EventBusName" : EVENT_BUS_NAME        
    }

    # pdb.set_trace()
    return event_bridge_event
