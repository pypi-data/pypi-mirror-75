from rest_framework import serializers
from dcim.api.nested_serializers import NestedDeviceSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer

from ..models import Lifecycle, LifecycleActionType

class LifecycleActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifecycleActionType
        fields = ['id', 'name']

class LifecycleSerializer(serializers.ModelSerializer):
    action_type = LifecycleActionTypeSerializer()
    device = NestedDeviceSerializer()
    user = NestedTenantSerializer()

    class Meta:
        model = Lifecycle
        fields = ['id', 'date', 'device', 'user', 'action_type']
