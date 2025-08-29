from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('vendor', 'Vendor'),
        ('engineer', 'Engineer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    alternative_email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    show_contact = models.BooleanField(default=False)  # If True, visible when tapped on post sender
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    


# This model stores additional user profile information separate from the core user model.
class UserProfile(models.Model):
    """
    Extends the CustomUser model with additional profile information.
    It is linked to a user via a OneToOne relationship.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    alternative_email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    show_contact = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        """String representation of the UserProfile model."""
        return self.user.username
