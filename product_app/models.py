from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class PurchaseHistory(models.Model):
    confirmation_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    fullName = models.CharField(max_length=65)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    quantityTickets = models.IntegerField(blank=True, null=True)
    
    
    def __unicode__(self):
          return u'%s - %s' % (self.name, self.confirmation_code)
      


    def total_price(self):
        return "%.2f" % float(float(self.price)*self.quantityTickets)
    