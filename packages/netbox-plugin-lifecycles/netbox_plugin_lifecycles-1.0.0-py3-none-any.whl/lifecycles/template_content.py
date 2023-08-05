from extras.plugins import PluginTemplateExtension
from .models import Lifecycle

class DeviceLifecyclesButton(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        return self.render('lifecycles/inc/device_lifecycles.html', extra_context={
	'lifecycles':Lifecycle.objects.filter(device_id=self.context['object'].id).all(),
	'device': self.context['object'].id
        })

template_extensions = [DeviceLifecyclesButton]
