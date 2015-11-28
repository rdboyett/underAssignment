from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class PurchaseHistory(models.Model):
    fullName = models.CharField(max_length=65)
    confirmation_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    phone = models.CharField(max_length=15, blank=True)
    
    
    def __unicode__(self):
          return u'%s - %s' % (self.name, self.confirmation_code)
      



admin.site.register(PurchaseHistory)
