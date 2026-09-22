from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_date = models.DateField(auto_now_add=True,auto_now=False)
    modified_date = models.DateField(auto_now_add=False,auto_now=True)
    historical = HistoricalRecords()

    class Meta:
        abstract = True