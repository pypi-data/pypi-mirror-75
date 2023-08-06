from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin

from utilities.views import BulkDeleteView, ObjectDeleteView, ObjectEditView, ObjectListView
from dcim.models import Device

from .models import Lifecycle, LifecycleActionType
from . import tables, filters, forms

class LifecycleView(PermissionRequiredMixin, View):
    permission_required = 'lifecycles.view_lifecycle'

    def get(self, request, pk):
        lifecycle = get_object_or_404(Lifecycle, id=pk)
        return render(request, 'lifecycles/lifecycle.html', {
            'lifecycle': lifecycle
        })

class LifecyclesView(PermissionRequiredMixin, ObjectListView):
  permission_required = 'lifecycles.view_lifecycle'
  queryset = Lifecycle.objects.prefetch_related('device')
  filterset = filters.LifecyclesFilter
  filterset_form = forms.LifecyclesFilterForm
  table = tables.LifecyclesTable
  template_name = 'lifecycles/lifecycles_list.html'

class LifecyclesCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'lifecycles.add_lifecycle'
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
  permission_required = 'lifecycles.change_lifecycle'


class LifecyclesBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'lifecyclese.delete_lifecycle'
    queryset = Lifecycle.objects.all()
    filter = filters.LifecyclesFilter
    table = tables.LifecyclesTable
    default_return_url = 'plugins:lifecycles:lifecycles'


class LifecyclesDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'lifecycles.delete_lifecycle'
    model = Lifecycle
    default_return_url = 'plugins:lifecycles:lifecycles'

class LifecycleActionTypesView(PermissionRequiredMixin, ObjectListView):
  permission_required = 'lifecycles.view_lifecycleactiontype'
  queryset = LifecycleActionType.objects.all()
  filterset = filters.LifecycleActionTypesFilter
  filterset_form = forms.LifecycleActionTypesFilterForm
  table = tables.LifecycleActionTypesTable
  template_name = 'lifecycles/lifecycle_action_types_list.html'

class LifecycleActionTypesCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'lifecycles.add_lifecycleactiontype'
    model = LifecycleActionType
    model_form = forms.LifecycleActionTypesCreateForm
    template_name = 'lifecycles/lifecycle_action_types_edit.html'
    default_return_url = 'plugins:lifecycles:lifecycle_action_types'

class LifecycleActionTypesEditView(LifecycleActionTypesCreateView):
  permission_required = 'lifecycles.change_lifecycleactiontype'

class LifecycleActionTypesBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'lifecyclese.delete_lifecycleactiontype'
    queryset = LifecycleActionType.objects.all()
    filter = filters.LifecycleActionTypesFilter
    table = tables.LifecycleActionTypesTable
    default_return_url = 'plugins:lifecycles::lifecycle_action_types'


class LifecycleActionTypesDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'lifecycles.delete_lifecycleactiontype'
    model = LifecycleActionType
    default_return_url = 'plugins:lifecycles::lifecycle_action_types'
