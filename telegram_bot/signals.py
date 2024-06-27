import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Car

print("Signals module loaded")

@receiver(pre_save, sender=Car)
def delete_old_file(sender, instance, **kwargs):
    if not instance.pk:
        return  # If instance is new and doesn't have a primary key yet, exit

    try:
        old_car = Car.objects.get(pk=instance.pk)
    except Car.DoesNotExist:
        return  # If old instance doesn't exist, exit

    old_file = old_car.photo
    new_file = instance.photo

    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(post_delete, sender=Car)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)
