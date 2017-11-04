from django.shortcuts import render
from .models import AccountID
from .serializers import AccountIDSerializer

from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

def account_id(request, account_id):
    account_id = AccountID.objects.get(account_id=account_id)
    return render(request, 'base.html', {'account_id':account_id})



class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer
    lookup_field = 'account_id'