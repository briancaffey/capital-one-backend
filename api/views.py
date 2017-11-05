# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import AccountID
from .serializers import AccountIDSerializer
from django.http import JsonResponse

from api import utils
# from . import utils
from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

from django.http import JsonResponse


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

def api_request(request, customer_id):
    data = utils.get_customer_info(customer_id=int(customer_id)).json()[0]
    customer, account_id = data["customers"][0], data["account_id"]

    if customer.get("is_primary", False):
        customers = utils.get_transaction_info(account_id=account_id).json()[0]["customers"]
        for customer in customers: 
            customer_info = utils.get_customer_info(customer_id=int(customer["customer_id"])).json()[0]["customers"][0]
            customer = {**customer, **customer_info}
         
    return JsonResponse(data, safe=False)


def list_transaction_info(request, account_id):
    data = utils.get_transaction_info(int(account_id))

    context = {
        'json':data
    }


class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer
    lookup_field = 'account_id'
