import django_filters

from . import models
from utilities.filters import TagFilter

from dcim.models import Device
from tenancy.models import Tenant

class LifecycleActionTypesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name',
    )

    class Meta:
        model = models.LifecycleActionType
        fields = ['id', 'name']

class LifecyclesFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='icontains',
        label='Date',
    )

    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device_id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device ID',
    )

    action_type = django_filters.ModelMultipleChoiceFilter(
        field_name='action_type_id',
        queryset=models.LifecycleActionType.objects.all(),
        to_field_name='id',
        label='Action Type ID',
    )

    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user_id',
        queryset=Tenant.objects.all(),
        to_field_name='id',
        label='User ID',
    )

    tag = TagFilter()

    class Meta:
        model = models.Lifecycle
        fields = ['id', 'date']
