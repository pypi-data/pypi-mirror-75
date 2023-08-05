from django.db import models
from djangoldp.models import Model


class MultiLingualModel(Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta(Model.Meta):
        anonymous_perms = ['view', 'add', 'delete', 'change', 'control']
        authenticated_perms = ['inherit']
        owner_perms = ['inherit']


class MultiLingualChild(Model):
    parent = models.ForeignKey(MultiLingualModel, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta(Model.Meta):
        anonymous_perms = ['view', 'add', 'delete', 'change', 'control']
        authenticated_perms = ['inherit']
        owner_perms = ['inherit']
        lookup_field = 'id'
