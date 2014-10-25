from django.db import models

# Create your models here.

class Client(models.Model):
	"""docstring for Question"""
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	rut = models.CharField(max_length=200)
	phone = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name
