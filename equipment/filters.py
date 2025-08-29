import django_filters
from .models import InstalledEquipment, STATUS_CHOICES, CATEGORY_CHOICES


class EquipmentFilter(django_filters.FilterSet):
    # Filter by name (partial match)
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label="Equipment Name"
    )

    # Filter by status using global STATUS_CHOICES
    status = django_filters.ChoiceFilter(
        field_name='status', choices=STATUS_CHOICES, label="Status"
    )

    # Filter by category
    category = django_filters.ChoiceFilter(
        field_name='category', choices=CATEGORY_CHOICES, label="Category"
    )

    # Date range filter for installed date
    installed_date = django_filters.DateFromToRangeFilter(
        field_name='date_installed', label="Installed Date (range)"
    )

    class Meta:
        model = InstalledEquipment
        fields = ['name', 'status', 'category', 'installed_date']
