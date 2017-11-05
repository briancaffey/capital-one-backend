# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .models import AccountID
from .serializers import AccountIDSerializer
from django.http import JsonResponse



from concurrent.futures import ThreadPoolExecutor

import json
import os


from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient


from api import utils
# from . import utils
from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

from django.http import JsonResponse

CCN = 'credit_card_number'
CID = 'customer_id'

env = os.environ.get("MONGODB_URI", 'mongodb://localhost:27017/codefam')
db_name = env.split('/')[-1]
client = MongoClient(env)
db = client[db_name]
users = db.users



def account_id(request, account_id):
    account_id = AccountID.objects.get(account_id=account_id)
    return render(request, 'base.html', {'account_id': account_id})


def get_customer_info(customer_id):
    data = utils.get_customer_info(customer_id=int(customer_id)).json()[0]
    return (data["customers"][0], data["account_id"])


def map_to_get_customer(customer):
    customer_info, account_id = get_customer_info(customer["customer_id"])
    return {**customer, **customer_info}

@csrf_exempt
def update_transaction(request):
    body = json.loads(request.body.decode())
    
    customer_id = int(body["customer_id"])
    transaction_id = int(body["transaction_id"])
    rating = body["rating"]
    try:
        transactions = users.find_one({"customer_id": int(customer_id)})["transactions"]

        updated_transactions = []
        for transaction in transactions:
            
            if transaction["transaction_id"] == transaction_id:
                updated_transactions.append({**transaction, "rating":rating})
            else: 
                updated_transactions.append(transaction)
        response = users.update_one({"customer_id": customer_id}, {"$set": {"transactions":updated_transactions}})

        return JsonResponse({"status":f'{response.modified_count} item(s) were updated'})

    except KeyError as error:
        
        return JsonResponse({"error":"failed to find record"})

def api_request(request, customer_id):
    try:
        db_user = users.find_one({"customer_id": int(customer_id)})
        if db_user:
            db_user["_id"] = str(db_user["_id"])
            return JsonResponse(db_user)

        customer, account_id = get_customer_info(customer_id)
        customer["account"] = utils.get_account_info(account_id).json()[0]

        rewards = utils.get_rewards_info(account_id).json()[0]["rewards"]
        customer["account"]["rewards"] = rewards

        transaction_info = utils.get_transaction_info(customer_id=customer_id)
        transaction_info = transaction_info.json()[0]["customers"][0]
        customer = {**customer, **transaction_info}

        if customer.get("is_primary", False):
            customers = utils.get_transaction_info(account_id=account_id)
            customers = customers.json()[0]["customers"]

            with ThreadPoolExecutor() as executor:
                filled_customers = executor.map(map_to_get_customer, customers,
                                                timeout=3)

            authorized = customer["account"]["authorized_users"]
            authorized = {user[CID]: {CCN: user[CCN]} for user in authorized}

            final_customers = [{**cus, **authorized[cus[CID]]}
                               for cus in filled_customers
                               if cus[CID] != customer[CID]]

            customer["account"]["authorized_users"] = final_customers

        response = JsonResponse(customer, safe=False)
        record_id = users.insert(customer)

        return response

    except IndexError as err:
        return JsonResponse({"error": "User doesn't exist."}, safe=False)


def list_transaction_info(request, account_id):
    data = utils.get_transaction_info(int(account_id))

    context = {
        'json': data
    }


class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer
    lookup_field = 'account_id'
