from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M','male'),
        ('F','female'),
        ('O','others')
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)
    nationality = models.CharField(max_length=40)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
