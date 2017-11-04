from django.shortcuts import render
from .models import AccountID
from .serializers import AccountIDSerializer

from rest_framework.generics import (
    RetrieveAPIView,
)
# Create your views here.

def account_id(request, id):
    id = AccountID.objects.get(id=id)
    return render(request, 'base.html', {'account_id':id})



class AccountIDDetailAPIView(RetrieveAPIView):
    queryset = AccountID.objects.all()
    serializer_class = AccountIDSerializer