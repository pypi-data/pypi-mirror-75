
# I18nLDPViewSet

I18nLDPViewSet overrides DjangoLDP's LDPViewSet to provide serialization using the I18nLDPSerializer, instead of the default LDPSerializer

You can activate the custom functionality on your DjangoLDP Model by setting `view_set` in the Model.Meta: https://git.startinblox.com/djangoldp-packages/djangoldp#view_set

# I18nLDPSerializer

The main functionality of I18n is provided in the serializer, which overrides DjangoLDP's LDPSerializer to select the activated language content and display this in the context of the response

The language is selected and the data manipulated automatically, based on the request object in the serializer context. A feature to provide the serialization into a language using a setting (without a request object) is TODO

# DjangoLDPI18nAdmin

This admin class simply inherits from `DjangoLDPAdmin` from DjangoLDP and `TranslationAdmin` from [Django-Modeltranslation](https://django-modeltranslation.readthedocs.io/en/latest/admin.html) to provide the features from both. It does so without additions
