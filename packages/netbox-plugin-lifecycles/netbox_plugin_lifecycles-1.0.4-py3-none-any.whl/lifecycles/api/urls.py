from rest_framework import routers
from . import views

class LifecyclesRootView(routers.APIRootView):
    def get_view_name(self):
        return 'Lifecycles'

router = routers.DefaultRouter()
router.APIRootView = LifecyclesRootView
router.register('lifecycles', views.LifecycleViewSet)
router.register('lifecycle_action_types', views.LifecycleActionTypeViewSet)
urlpatterns = router.urls
