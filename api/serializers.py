from rest_framework.serializers import ModelSerializer

from .models import AccountID

class AccountIDSerializer(ModelSerializer):

    class Meta:
        model = AccountID
        fields = [
            'account_id'
        ]