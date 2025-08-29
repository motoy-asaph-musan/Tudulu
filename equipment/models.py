# equipment/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# --- Model Choices ---
# Choices for the equipment category
CATEGORY_CHOICES = [
    ('electrical', 'Electrical'),
    ('mechanical', 'Mechanical'),
    ('software', 'Software'),
    ('radiology', 'radiology'),
    ('ICU', 'ICU'),
    ('Triage', 'Triage'),
    ('Physiotherapy', 'Physiotherapy'),
    ('HDU', 'HDU'),
    ('Laboratory', 'Laboratory'),
    ('other', 'Other'),
]

# Choices for the equipment status
STATUS_CHOICES = [
    ('active', 'Active'),
    ('available', 'Available'),
    ('maintenance', 'In Maintenance'),
    ('retired', 'Decommissioned'),
]

# Choices for task status
TASK_STATUS = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
]

# ---------------------------
# Core Equipment Models
# ---------------------------
class InstalledEquipment(models.Model):
    """
    Model to track equipment that has been installed or is owned.
    It includes details like service dates and status.
    """
    # Owner of the equipment (linked to the custom user model)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_equipment'
    )
    # The person who added this record (can be different from the owner)
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
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current operational status of the equipment"
    )

    # Property methods to check service due dates
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

    # Custom validation to ensure data integrity
    def clean(self):
        if self.status == 'retired' and not self.date_installed:
            raise ValidationError("Retired equipment must have an installation date")
        if self.next_service_date and self.last_service_date:
            if self.next_service_date < self.last_service_date:
                raise ValidationError("Next service date cannot be before last service date")

    def get_absolute_url(self):
        return reverse('equipment:equipment_detail', args=[self.pk])

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    class Meta:
        ordering = ['-date_installed', 'name']
        verbose_name_plural = 'Installed Equipment'


# ---------------------------
# Social Features
# ---------------------------
class Post(models.Model):
    """
    Model for social posts related to equipment.
    Includes a check to restrict image uploads to premium users.
    """
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=255)
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
        # A check for premium users, assuming UserProfile exists
        if self.image and not self.author.userprofile.is_premium:
            raise PermissionDenied("Uploading images is for premium users only.")
        super().save(*args, **kwargs)


class Like(models.Model):
    """
    Model for users to 'like' a post.
    """
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
        
    def __str__(self):
        return f'{self.user.username} liked {self.post.title}'


class Comment(models.Model):
    """
    Model for users to comment on a post.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    # post = models.ForeignKey(
    #     Post,
    #     on_delete=models.CASCADE,
    #     related_name='post_comments'
    # )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"


# ---------------------------
# Task and Notification Models
# ---------------------------
class Task(models.Model):
    """
    Model for a to-do list or maintenance task related to a piece of equipment.
    """
    equipment = models.ForeignKey(
        InstalledEquipment,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS,
        default='pending'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks_assigned"
    )

    @property
    def is_overdue(self):
        return self.due_date and date.today() > self.due_date and self.status != 'done'

    @property
    def is_due_soon(self):
        return (
            self.due_date
            and date.today() + timedelta(days=3) >= self.due_date
            and not self.is_overdue
            and self.status != 'done'
        )

    def __str__(self):
        return f"Task: {self.title} ({self.equipment.name})"

    class Meta:
        ordering = ['due_date', 'status']


class DueNotification(models.Model):
    """
    Model to handle notifications for due dates on equipment.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='due_notifications')
    equipment = models.ForeignKey(
        'InstalledEquipment',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    due_date = models.DateField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.equipment.name} to {self.user.username}"



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("maintenance", "Maintenance Due"),
        ("like", "Like"),
        ("comment", "Comment"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="actor_notifications"
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    equipment = models.ForeignKey("InstalledEquipment", on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient} - {self.notification_type}"
# ---------------------------
# Transaction Model
# ---------------------------
class Transaction(models.Model):
    """
    Model to track transactions, such as equipment rental payments.
    This model now correctly references the custom user model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"
