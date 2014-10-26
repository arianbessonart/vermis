from django.db import models

# Create your models here.

class Contact(models.Model):
	"""docstring for Contact"""
	f_name = models.CharField(max_length=200)
	l_name = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)

	def __unicode__(self):
		return "%s %s"%(self.f_name,self.l_name)
