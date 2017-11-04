from django.db import models

# Create your models here.

class AccountID(models.Model): 
    account_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.account_id)