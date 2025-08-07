from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class InstalledEquipment(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    date_installed = models.DateField()
    next_service_date = models.DateField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='equipment_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} at {self.location}"

POST_TAGS = [
    ('sale', 'For Sale'),
    ('rent', 'For Rent'),
    ('donation', 'Donation'),
]

class EquipmentPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    tag = models.CharField(max_length=20, choices=POST_TAGS, default='sale')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(EquipmentPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(EquipmentPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

