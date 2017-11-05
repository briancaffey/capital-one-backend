# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import AccountID
from .serializers import AccountIDSerializer
from django.http import JsonResponse

from concurrent.futures import ThreadPoolExecutor

from api import utils
# from . import utils
from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

from django.http import JsonResponse


#mongodb
import pymongo
mongo_uri = "mongodb://contingency:qwer1234@cluster0-shard-00-00-xisxs.mongodb.net:27017,cluster0-shard-00-01-xisxs.mongodb.net:27017,cluster0-shard-00-02-xisxs.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
client = pymongo.MongoClient(mongo_uri)

db = client.test



# import requests
# import json

# base_url = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon/'


# def get_account_info(account_id):
#     option = 'accounts'
#     body = {"account_id": int(account_id)}
#     info = requests.post(base_url + option, data=json.dumps(body))
#     return info

def account_id(request, account_id):
    account_id = AccountID.objects.get(account_id=account_id)
    return render(request, 'base.html', {'account_id':account_id})

def get_customer_info(customer_id):
    data = utils.get_customer_info(customer_id=int(customer_id)).json()[0]
    return (data["customers"][0], data["account_id"])
    
def map_to_get_customer(customer):
    customer_info, account_id = get_customer_info(customer["customer_id"])
    return {**customer, **customer_info}


def api_request(request, customer_id):

    

    try: 
        customer, account_id = get_customer_info(customer_id)

        customer["account"] = utils.get_account_info(account_id).json()[0]
        transaction_info = utils.get_transaction_info(customer_id=customer_id).json()[0]["customers"][0]
        customer = {**customer, **transaction_info}

        if customer.get("is_primary", False):
            customers = utils.get_transaction_info(account_id=account_id).json()[0]["customers"]
            
            # filled_customers = []
            with ThreadPoolExecutor() as executor:
                filled_customers = executor.map(map_to_get_customer, customers, timeout=3)

            authorized = customer["account"]["authorized_users"]

            authorized = {user['customer_id']:{"credit_card_number":user['credit_card_number']} for user in authorized }
            print(authorized)
            final_customers = [{**cus, **authorized[cus["customer_id"]]} for cus in filled_customers if cus["customer_id"] != customer["customer_id"]]
        
            customer["account"]["authorized_users"] = final_customers

        return JsonResponse(customer, safe=False)
    except IndexError as err: 
        return JsonResponse({"error":"User doesn't exist."}, safe=False)


def list_transaction_info(request, account_id):
    data = utils.get_transaction_info(int(account_id))

    context = {
        'json':data
    }


class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer
    lookup_field = 'account_id'
