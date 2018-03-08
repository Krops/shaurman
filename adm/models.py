from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=200)
    restaurant = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    date = models.DateTimeField()
    amount = models.IntegerField(default=1)

    def __str__(self):
        return "{} - {} for {} at {}".format(self.product, self.amount, self.user, self.date)
