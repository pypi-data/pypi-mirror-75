from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from utilities.views import BulkDeleteView, ObjectDeleteView, ObjectEditView, ObjectListView
from dcim.models import Device

from .models import Lifecycle, LifecycleActionType
from . import tables, filters, forms

class LifecycleView(PermissionRequiredMixin, View):
    permission_required = 'lifecycles.lifecycles'

    def get(self, request, pk):
        lifecycle = get_object_or_404(Lifecycle, id=pk)
        return render(request, 'lifecycles/lifecycle.html', {
            'lifecycle': lifecycle
        })


class LifecyclesView(PermissionRequiredMixin, ObjectListView):
  permission_required = 'lifecycles.lifecycles'
  queryset = Lifecycle.objects.prefetch_related('device')
  filterset = filters.LifecyclesFilter
  filterset_form = forms.LifecyclesFilterForm
  table = tables.LifecyclesTable
  template_name = 'lifecycles/lifecycles_list.html'

class LifecyclesCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'lifecycles.lifecycles_create'
    model = Lifecycle
    model_form = forms.LifecyclesCreateForm
    template_name = 'lifecycles/lifecycles_edit.html'
    default_return_url = 'plugins:lifecycles:lifecycles'

    def alter_obj(self, obj, request, url_args, url_kwargs):
        if 'device' in request.GET:
            obj.device = get_object_or_404(Device, pk=request.GET['device'])
        return obj

    def get_return_url(self, request, service):
        if 'device' in request.GET:
            return '/dcim/devices/'+str(request.GET['device'])+'/'
        else:
            return '/plugins/lifecycles/lifecycles/'

class LifecyclesEditView(LifecyclesCreateView):
  permission_required = 'lifecycles.lifecycles_edit'


class LifecyclesBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'lifecyclese.lifecycles_delete'
    queryset = Lifecycle.objects.all()
    filter = filters.LifecyclesFilter
    table = tables.LifecyclesTable
    default_return_url = 'plugins:lifecycles:lifecycles'


class LifecyclesDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'lifecycles.lifecycles_delete'
    model = Lifecycle
    default_return_url = 'plugins:lifecycles:lifecycles'

class LifecycleActionTypesView(PermissionRequiredMixin, ObjectListView):
  permission_required = 'lifecycles.lifecycle_action_types'
  queryset = LifecycleActionType.objects.all()
  filterset = filters.LifecycleActionTypesFilter
  filterset_form = forms.LifecycleActionTypesFilterForm
  table = tables.LifecycleActionTypesTable
  template_name = 'lifecycles/lifecycle_action_types_list.html'

class LifecycleActionTypesCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'lifecycles.lifecycle_action_types_create'
    model = LifecycleActionType
    model_form = forms.LifecycleActionTypesCreateForm
    template_name = 'lifecycles/lifecycle_action_types_edit.html'
    default_return_url = 'plugins:lifecycles:lifecycle_action_types'

class LifecycleActionTypesEditView(LifecycleActionTypesCreateView):
  permission_required = 'lifecycles.lifecycle_action_types_edit'

class LifecycleActionTypesBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'lifecyclese.lifecycle_action_types_delete'
    queryset = LifecycleActionType.objects.all()
    filter = filters.LifecycleActionTypesFilter
    table = tables.LifecycleActionTypesTable
    default_return_url = 'plugins:lifecycles::lifecycle_action_types'


class LifecycleActionTypesDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'lifecycles.lifecycle_action_type_delete'
    model = LifecycleActionType
    default_return_url = 'plugins:lifecycles::lifecycle_action_types'
