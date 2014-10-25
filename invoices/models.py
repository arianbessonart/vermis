from django.db import models
from clients.models import Client

from datetime import datetime

# Create your models here.

class Invoice(models.Model):
	"""docstring for Invoice"""
	sub_total = models.FloatField(default=0.0)
	iva = models.FloatField(default=0.0)
	total = models.FloatField(default=0.0)
	reference_name = models.CharField(max_length=200,null = True)
	reference_number = models.IntegerField(default=0)
	date_created = models.DateField()
	date_added = models.DateTimeField(default=datetime.now)
	date_edited = models.DateTimeField(default=datetime.now)
	charged = models.BooleanField(default=False)
	date_charged = models.DateField(null = True)
	client = models.ForeignKey(Client, null = True, blank = True)

	def __unicode__(self):
		return str(self.reference_number)

class Item(models.Model):
	"""docstring for Item"""
	description = models.CharField(max_length=200)
	price = models.FloatField(default=0.0)
	invoice = models.ForeignKey(Invoice, null = True, blank = True)

	def __unicode__(self):
		return str(self.description)