from django.db import models

# Create your models here.

class Empdetails(models.Model):
    empid=models.IntegerField()
    empname=models.CharField(max_length=64)
    empcity=models.CharField(max_length=64)

    def __str__(self):
        return self.empname

