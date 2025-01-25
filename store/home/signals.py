# home/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer

# Signal handler to create a customer when a new user is created
'''
i had a problem whenever i created a user with the authentication tab,
it did not generate customer so i used signals.py and i also added the function to the app.py file
'''
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:  # If a new user is created
        Customer.objects.create(
            user=instance,
            name=instance.username,  # Use the username as the customer's name
            email=instance.email,    # Use the user's email
            phone_number=instance.first_name        # Set phone number
        )
