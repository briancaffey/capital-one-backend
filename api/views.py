from django.shortcuts import render
from .models import AccountID
from .serializers import AccountIDSerializer
from django.http import JsonResponse

#from api import utils
# from . import utils
from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

import requests
import json

base_url = 'https://3hkaob4gkc.execute-api.us-east-1.amazonaws.com/prod/au-hackathon/'


def get_account_info(account_id):
    print("working")
    print(account_id)
    option = 'accounts'
    body = {"account_id": account_id}
    info = requests.post(base_url + option, data=json.dumps(body))
    print(info)
    print(info.json())
    return info.json()

def account_id(request, account_id):
    account_id = AccountID.objects.get(account_id=account_id)
    return render(request, 'base.html', {'account_id':account_id})

def api_request(request, account_id):
    data = get_account_info(account_id)
    context = {
        'account_id':account_id,
        'json':data
    }
    # JsonResponse(data)
    return render(request, 'api_request.html', context)


class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer
    lookup_field = 'account_id'
