from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:lifecycles:lifecycles',
        link_text='Lifecycles',
        buttons=(
            PluginMenuButton('plugins:lifecycles:lifecycle_add', 'Add lifecycle', 'fa fa-plus', ButtonColorChoices.GREEN),
        )
    ),
    PluginMenuItem(
        link='plugins:lifecycles:lifecycle_action_types',
        link_text='Lifecycle Action Types',
        buttons=(
            PluginMenuButton('plugins:lifecycles:lifecycle_action_type_add', 'Add lifecycle action type', 'fa fa-plus', ButtonColorChoices.GREEN),
        )
    )
)
