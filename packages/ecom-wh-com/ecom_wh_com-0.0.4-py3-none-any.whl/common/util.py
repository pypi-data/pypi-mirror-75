import json,datetime
import copy,uuid,os


def enrich_inventory(inventory_item):

    now =  datetime.datetime.now()

    id  = str(uuid.uuid4())    

    inventory_item["PK"] =  "INVENTORY#{}".format(inventory_item["productId"])
    inventory_item["SK"] =  "INVENTORY"
    inventory_item["GSK1-PK"] =  "OFF"
    inventory_item["GSK1-SK"] =  now.isoformat()
    inventory_item["updatedDateTime"] =   now.isoformat()

    return inventory_item

