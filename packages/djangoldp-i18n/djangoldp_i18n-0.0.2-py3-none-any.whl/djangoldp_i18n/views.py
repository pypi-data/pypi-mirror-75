from django.utils.decorators import classonlymethod
from djangoldp.views import LDPViewSet, LDPNestedViewSet
from djangoldp_i18n.serializers import I18nLDPSerializer, I18nContainerSerializer


class I18nLDPViewSet(LDPViewSet):
    '''
    Overrides LDPViewSet to use custom serializer
    '''

    def build_serializer(self, meta_args, name_prefix):
        # create the Meta class to associate to LDPSerializer, using meta_args param
        if self.fields:
            meta_args['fields'] = self.fields
        else:
            meta_args['exclude'] = self.exclude or ()
        meta_args['list_serializer_class'] = I18nContainerSerializer
        meta_class = type('Meta', (), meta_args)

        return type(I18nLDPSerializer)(self.model._meta.object_name.lower() + name_prefix + 'Serializer',
                                       (I18nLDPSerializer,),{'Meta': meta_class})

    @classonlymethod
    def nested_urls(cls, nested_field, **kwargs):
        return I18nLDPNestedViewSet.nested_urls(nested_field, **kwargs)


class I18nLDPNestedViewSet(LDPNestedViewSet, I18nLDPViewSet):
    pass
