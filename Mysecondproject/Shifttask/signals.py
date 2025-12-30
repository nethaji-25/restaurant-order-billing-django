from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShiftAssignment
from .google_sheet_utils import update_google_sheet

@receiver(post_save,sender=ShiftAssignment)
def sync_to_google_sheet(sender,instance,**kwargs):
    update_google_sheet(employee_name=instance.employee.name)