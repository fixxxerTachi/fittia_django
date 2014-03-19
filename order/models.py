from django.db import models
from products.models import *
from payment.models import Select
from django.contrib.auth.models import User
class NoUser(models.Model):
	name=models.CharField(max_length=255)
	zip_first=models.PositiveIntegerField()
	zip_last=models.PositiveIntegerField()
	address=models.CharField(max_length=255)
	email=models.EmailField()
	level_r=models.DecimalField(max_digits=5,decimal_places=2,default=None)
	level_l=models.DecimalField(max_digits=5,decimal_places=2,default=None)
	astig_r=models.DecimalField(max_digits=5,decimal_places=2,default=None)
	astig_l=models.DecimalField(max_digits=5,decimal_places=2,default=None)

class Orders(models.Model):
	bought=models.ManyToManyField(Products,through='OrdersInfo')
	payment=models.ForeignKey(Select)
	customer=models.ForeignKey(NoUser)
	user=models.ForeignKey(User)

class OrdersInfo(models.Model):
	product=models.ForeignKey(Products)
	orders=models.ForeignKey(Orders)
	lens_type=models.CharField(max_length=10)
	no_lens=models.ForeignKey(NoLens)
	leveled_lens=models.ForeignKey(LeveledLens)
