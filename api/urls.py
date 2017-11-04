from django.conf.urls import url, include
from django.contrib import admin

from api import views

from .views import (
    AccountIDDetailAPIView,
)

urlpatterns = [
    url(r'^(?P<account_id>\d+)/$', views.account_id, name="account_id"),
    url(r'^v1/(?P<account_id>\d+)/$', AccountIDDetailAPIView.as_view(), name='detail'),
]
