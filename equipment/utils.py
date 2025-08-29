# equipment/utils.py
from django.utils import timezone
from .models import InstalledEquipment, Notification

def check_equipment_notifications():
    today = timezone.now().date()
    equipments = InstalledEquipment.objects.filter(next_service_date__lte=today)

    for equipment in equipments:
        Notification.objects.get_or_create(
            user=equipment.user,   # owner of equipment
            notification_type="maintenance",
            message=f"Equipment '{equipment.name}' is due for maintenance.",
        )
