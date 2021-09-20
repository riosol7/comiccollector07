from django.db.models.signals import post_save ##django save method
from django.contrib.auth.models import User
from django.dispatch import receiver ## receiver decorator, a signal or a list of signals to connect a function to.
from .models import Profile

## https://docs.djangoproject.com/en/3.2/ref/signals/
## Django recommends to write all signal operations in signals.py
## signals are comprised of senders and receivers that send out information to receivers / similar to how an event listener operates.
## when a post_save signal is receive, function will operate

##parameter of sender is equal to a model class which is defined as User model
@receiver(post_save, sender=User)
## have the arguments of sender, instance of the model: object that is sending out the information, created: which checks to see if a new record was created or if was an update.
## **kwargs a convention variable which passes keyworded variable length of arguments to a function.
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()