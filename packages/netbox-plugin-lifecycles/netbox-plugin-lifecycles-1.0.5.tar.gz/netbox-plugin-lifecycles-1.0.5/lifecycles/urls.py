from django.urls import path
from . import views, models

from extras.views import ObjectChangeLogView

urlpatterns = [
    path('lifecycles/<int:pk>/', views.LifecycleView.as_view(), name='lifecycle'),
    path('lifecycles/create/', views.LifecyclesCreateView.as_view(), name='lifecycle_add'),
    path('lifecycles/', views.LifecyclesView.as_view(), name='lifecycles'),
    path('lifecycles/delete/', views.LifecyclesBulkDeleteView.as_view(), name='lifecycle_bulk_delete'),
    path('lifecycles/<int:pk>/delete/', views.LifecyclesDeleteView.as_view(), name='lifecycle_delete'),
    path('lifecycles/<int:pk>/edit/', views.LifecyclesEditView.as_view(), name='lifecycle_edit'),
    path('lifecycles/<int:pk>/changelog/',  ObjectChangeLogView.as_view(), name='lifecycle_changelog', kwargs={'model':models.Lifecycle}),

    path('lifecycle_action_types/create/', views.LifecycleActionTypesCreateView.as_view(), name='lifecycle_action_type_add'),
    path('lifecycle_action_types/', views.LifecycleActionTypesView.as_view(), name='lifecycle_action_types'),
    path('lifecycle_action_types/delete/', views.LifecycleActionTypesBulkDeleteView.as_view(), name='lifecycle_action_type_bulk_delete'),
    path('lifecycle_action_types/<int:pk>/delete/', views.LifecycleActionTypesDeleteView.as_view(), name='lifecycle_action_type_delete'),
    path('lifecycle_action_types/<int:pk>/edit/', views.LifecycleActionTypesEditView.as_view(), name='lifecycle_action_type_edit'),
]
