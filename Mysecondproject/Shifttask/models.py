

from django.db import models

# Create your models here.

class Employee(models.Model):
    name=models.CharField(max_length=100)
    empid=models.IntegerField()

    def __str__(self):
        return self.name

class Shift(models.Model):
    shift_name=models.CharField(max_length=100)

    def __str__(self):
        return self.shift_name

class ShiftAssignment(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    from_date=models.DateField()
    to_date=models.DateField()

    def __str__(self):
        return f"{self.employee.name} - {self.shift.shift_name} ({self.from_date} to {self.to_date})"

