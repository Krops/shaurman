from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


class Product(models.Model):
    title = models.CharField(max_length=200)
    restaurant = models.CharField(max_length=200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='UAH')

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    date = models.DateTimeField()
    amount = models.IntegerField(default=1)

    def __str__(self):
        return "{} - {} for {} at {}".format(self.product, self.amount, self.user, self.date)
