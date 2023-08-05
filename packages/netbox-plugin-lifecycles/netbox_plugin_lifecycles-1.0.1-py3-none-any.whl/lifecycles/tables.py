from utilities.tables import BaseTable, ToggleColumn
import django_tables2 as tables
from django_tables2.utils import Accessor

from . import models

class LifecycleActionTypesTable(BaseTable):
    pk = ToggleColumn()

    actions = tables.TemplateColumn(
        template_name='lifecycles/lifecycle_action_types_buttons.html',
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta(BaseTable.Meta):
        model = models.LifecycleActionType
        fields = (
            'pk', 'name', 'actions'
        )

class LifecyclesTable(BaseTable):
    pk = ToggleColumn()
    device = tables.LinkColumn()

    id = tables.LinkColumn(
        viewname='plugins:lifecycles:lifecycle',
        args=[Accessor('pk')],
        verbose_name='ID'
    )

    actions = tables.TemplateColumn(
        template_name='lifecycles/lifecycles_buttons.html',
        attrs={'td': {'class': 'text-right noprint'}},
        verbose_name=''
    )

    class Meta(BaseTable.Meta):
        model = models.Lifecycle
        fields = (
            'pk', 'id', 'date', 'action_type', 'device', 'actions'
        )
