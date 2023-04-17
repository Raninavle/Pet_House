from django.db import models
from datetime import datetime
# Create your models here.

class MyCart(models.Model):
    user = models.ForeignKey(to='adminapp.UserInfo', on_delete=models.CASCADE)
    pet = models.ForeignKey(to='adminapp.Pet_Cat',on_delete=models.CASCADE)

    class Meta:
        db_table = "MyCart"


class OrderMaster(models.Model):
    user = models.ForeignKey(to='adminapp.UserInfo', 
              on_delete=models.CASCADE)
    amount = models.FloatField(default=1000)
    dateOfOrder = models.DateTimeField(default=datetime.now)
    details = models.CharField(max_length=200)
    class Meta:
        db_table  = "OrderMaster"