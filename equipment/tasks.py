# equipment/tasks.py
from datetime import date, timedelta
from django.conf import settings
from django.core.mail import send_mail
from .models import InstalledEquipment
from celery import shared_task
from django.utils import timezone
from .models import Equipment  # adjust import

def send_service_alerts():
    today = date.today()
    upcoming_date = today + timedelta(days=7)

    # Find equipment due in exactly 7 days
    due_soon = InstalledEquipment.objects.filter(next_service_date=upcoming_date)

    if due_soon.exists():
        subject = "Equipment Service Reminder: Equipment Due Soon"
        body = "The following equipment is due for service in 7 days:\n\n"
        # body += "\n".join([f"{eq.name} - Next service: {eq.next_service_date}" for eq in due_soon])
        for eq in due_soon:
            body += f"- {eq.name} ({eq.serial_number}) at {eq.location}, Next Service: {eq.next_service_date}\n"
            
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,  # sender
            settings.SERVICE_ALERT_RECIPIENTS,  # recipients
            fail_silently=False,
        )

@shared_task
def send_due_equipment_emails():
    today = timezone.now().date()
    due_items = Equipment.objects.filter(due_date=today)
    count = due_items.count()
    if count > 0:
        # send email logic here
        print(f"Sent emails for {count} due items.")
    else:
        print("No items due today.")
