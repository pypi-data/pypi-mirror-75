from django import forms

from utilities.forms import APISelect, BootstrapMixin, DynamicModelMultipleChoiceField, APISelectMultiple
from .models import Lifecycle, LifecycleActionType
from dcim.models import Device
from tenancy.models import Tenant

from extras.forms import TagField

class LifecyclesCreateForm(BootstrapMixin, forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = Lifecycle
        fields = [
            'id', 'date', 'user', 'device', 'action_type', 'comments', 'tags'
        ]
        widgets = {
            'device': APISelect(api_url='/api/dcim/devices/'),
            'user': APISelect(api_url='/api/tenancy/tenants/'),
            'action_type': APISelect(api_url='/api/plugins/lifecycles/lifecycle_action_types')
        }

class LifecycleActionTypesCreateForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = LifecycleActionType
        fields = [
            'name'
        ]
        widgets = { }

class LifecycleActionTypesFilterForm(BootstrapMixin, forms.Form):
    model = LifecycleActionType
    name = forms.CharField(
        required=False,
        label='Search'
    )

class LifecyclesFilterForm(BootstrapMixin, forms.Form):
    model = Lifecycle

    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        to_field_name='id',
        required=False,
        widget=APISelectMultiple(
            value_field="id",
        )
    )

    action_type = DynamicModelMultipleChoiceField(
        queryset=LifecycleActionType.objects.all(),
        to_field_name='id',
        required=False,
        widget=APISelectMultiple(
            api_url='/api/plugins/lifecycles/lifecycle_action_types',
            value_field="id",
        )
    )

    user = DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='id',
        required=False,
        widget=APISelectMultiple(
            value_field="id",
        )
    )


    date = forms.DateField(
        required=False,
        label='Date'
    )

