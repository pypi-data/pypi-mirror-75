from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:lifecycles:lifecycles',
        link_text='Lifecycles',
		permissions=['lifecycles.view_lifecycle'],
        buttons=(
            PluginMenuButton('plugins:lifecycles:lifecycle_add', 'Add lifecycle', 'fa fa-plus', ButtonColorChoices.GREEN,
							permissions=['lifecycles.add_lifecycle']),
        )
    ),
    PluginMenuItem(
        link='plugins:lifecycles:lifecycle_action_types',
        link_text='Lifecycle Action Types',
		permissions=['lifecycles.view_lifecycleactiontype'],
        buttons=(
            PluginMenuButton('plugins:lifecycles:lifecycle_action_type_add', 'Add lifecycle action type', 'fa fa-plus', ButtonColorChoices.GREEN,
							permissions=['lifecycles.add_lifecycleactiontype']),
        )
    )
)
