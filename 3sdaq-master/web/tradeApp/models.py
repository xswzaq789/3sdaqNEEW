from django.db import models

# Create your models here.
class Comp(models.Model):
    code    = models.IntegerField(primary_key = True)
    name  = models.CharField(max_length=500)
    type  = models.CharField(max_length=100)
    vol   = models.IntegerField(default=100)
    d_1price = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    u_date = models.DateTimeField(null=True)

class Order(models.Model):
    code = models.IntegerField()
    gubun  = models.CharField(max_length=1, default='B')
    price  = models.IntegerField(default=0)
    quan   = models.IntegerField(default=0)
    tquan = models.IntegerField(default=0, null=True)
    buyer  = models.CharField(max_length=50, null=True)
    seller = models.CharField(max_length=50, null=True)
    tradeyn = models.CharField(max_length=1, default='N')
    time1 = models.DateTimeField(auto_now=True)
    time2 = models.DateTimeField(null=True)

class Ballance(models.Model):
    user_id = models.CharField(max_length=50)
    code    = models.IntegerField()
    price  = models.IntegerField(default=0)
    quan   = models.IntegerField(default=0)
    t_price = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id","code"],
                name="unique ballance",
            )
        ]

class D_price(models.Model):
    day = models.CharField(max_length=50)
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)

class D_trade(models.Model):
    day = models.CharField(max_length=50, primary_key = True)
    volume = models.IntegerField(default=0)
    trade_cost = models.IntegerField(default=0)
    ex_index = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
















































