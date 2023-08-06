from django.db import models
from dcim.models import Device
from tenancy.models import Tenant
from taggit.managers import TaggableManager
from extras.models import CustomFieldModel, ObjectChange, TaggedItem
from utilities.models import ChangeLoggedModel

from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse


class LifecycleActionType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
          return getattr(self, 'name')

	def get_absolute_url(self):
           return reverse('plugins:lifecycles:lifecycle_action_types')

class Lifecycle(ChangeLoggedModel):
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(Tenant, on_delete=models.PROTECT, blank=True, null=True)
	device = models.ForeignKey(Device, on_delete=models.PROTECT)
	action_type = models.ForeignKey(LifecycleActionType, on_delete=models.PROTECT)

	def __str__(self):
          return str(getattr(self, 'date'))+': '+ getattr(self, 'action_type').name +' - '+ getattr(self, 'device').name

	comments = models.TextField(
           blank=True
        )

	tags = TaggableManager(through=TaggedItem)

	class Meta:
	   ordering = ['id']

	def get_absolute_url(self):
           return reverse('plugins:lifecycles:lifecycle', args=[self.id])
