from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        permissions = ['netbox_licences.view_softwareprovider'],
        link='plugins:netbox_licences:software_providers_list',
        link_text='Software Providers',
        buttons=(
            PluginMenuButton('home', 'Button A', 'fa fa-info', ButtonColorChoices.BLUE),
            PluginMenuButton('home', 'Button B', 'fa fa-warning', ButtonColorChoices.GREEN),
        )
    ),
    PluginMenuItem(
        permissions = ['netbox_licences.view_licence'],
        link='plugins:netbox_licences:licences_list',
        link_text='Licences',
    ),
)
