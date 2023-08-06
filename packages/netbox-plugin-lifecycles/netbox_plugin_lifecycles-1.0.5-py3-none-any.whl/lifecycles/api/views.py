from rest_framework.viewsets import ModelViewSet
from lifecycles.models import LifecycleActionType, Lifecycle
from .serializers import LifecycleActionTypeSerializer, LifecycleSerializer

class LifecycleActionTypeViewSet(ModelViewSet):
    queryset = LifecycleActionType.objects.all()
    serializer_class = LifecycleActionTypeSerializer

class LifecycleViewSet(ModelViewSet):
    queryset = Lifecycle.objects.all()
    serializer_class = LifecycleSerializer
