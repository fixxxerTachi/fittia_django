from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
	user=models.OneToOneField(User)
	first_furigana=models.CharField(max_length=100)
	last_furigana=models.CharField(max_length=100)
	zip_code_first=models.PositiveIntegerField()
	zip_code_last=models.PositiveIntegerField()
	prefecture=models.CharField(max_length=10)
	city=models.CharField(max_length=255)
	address=models.CharField(max_length=255)
	email=models.EmailField()

class Select(models.Model):
	payment=models.CharField(max_length=50)
	def __unicode__(self):
		return self.payment
