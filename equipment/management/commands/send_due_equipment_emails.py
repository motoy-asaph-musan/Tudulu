from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from equipment.models import InstalledEquipment

# Put your recipients here
RECIPIENTS = [
    "person1@example.com",
    "person2@example.com",
]

class Command(BaseCommand):
    help = "Send email alerts for equipment due soon or today"

    def handle(self, *args, **kwargs):
        today = now().date()
        one_week_from_now = today + timedelta(days=7)

        # Items due in 7 days
        due_soon = InstalledEquipment.objects.filter(next_service_date=one_week_from_now)
        # Items due today
        due_today = InstalledEquipment.objects.filter(next_service_date=today)

        # Send email for due soon
        if due_soon.exists():
            send_mail(
                subject="Equipment Service Reminder",
                message="\n".join([f"{item.name} - Service due on {item.next_service_date}" for item in due_soon]),
                from_email="your_email@example.com",
                recipient_list=RECIPIENTS,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Sent reminder emails for {due_soon.count()} items."))

        # Flag due today (you can add a boolean field like is_due=True)
        for item in due_today:
            item.status = "Due"  # Or set a boolean like item.is_due = True
            item.save()

        self.stdout.write(self.style.SUCCESS(f"Flagged {due_today.count()} items as due today."))
