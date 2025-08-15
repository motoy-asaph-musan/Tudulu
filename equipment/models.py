from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.core.exceptions import PermissionDenied

# ---------------------------
# Post, Like, Comment Models
# ---------------------------

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(
        max_length=20,
        choices=[
            ('sale', 'For Sale'),
            ('rent', 'For Rent'),
            ('donation', 'Donation'),
        ],
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"Post by {self.author.username}"

    def save(self, *args, **kwargs):
        if self.image and not self.author.profile.is_premium:
            raise PermissionDenied("Uploading images is for premium users only.")
        super().save(*args, **kwargs)
        
class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"


# ---------------------------
# Installed Equipment Model
# ---------------------------

CATEGORY_CHOICES = [
    ('electrical', 'Electrical'),
    ('mechanical', 'Mechanical'),
    ('software', 'Software'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('available', 'Available'),
    ('maintenance', 'In Maintenance'),
    ('retired', 'Decommissioned'),
]

class InstalledEquipment(models.Model):
    # The actual owner of the equipment (based on email in their account)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_equipment'
    )
    
    # The person who added the record (could be same as user or different)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_added'
    )

    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    date_installed = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='equipment_photos/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current operational status of the equipment"
    )

    @property
    def is_overdue(self):
        return self.next_service_date and date.today() >= self.next_service_date

    @property
    def is_due_soon(self):
        return (
            self.next_service_date
            and date.today() + timedelta(days=7) >= self.next_service_date
            and not self.is_overdue
        )

    def clean(self):
        if self.status == 'retired' and not self.date_installed:
            raise ValidationError("Retired equipment must have an installation date")
        if self.next_service_date and self.last_service_date:
            if self.next_service_date < self.last_service_date:
                raise ValidationError("Next service date cannot be before last service date")

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        ordering = ['-date_installed', 'name']
        verbose_name_plural = 'Installed Equipment'
