from django.contrib import admin

from models import *

#from django.db.models import get_models, get_app
#from django.contrib import admin
#from django.contrib.admin.sites import AlreadyRegistered

class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}

class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'submitter', None) is None:
            obj.submitter = request.user
        obj.save()

admin.site.register(resource_model, ResourceAdmin)
admin.site.register(subject_model)
admin.site.register(creator_model)
admin.site.register(contributor_model)
admin.site.register(date_model)
admin.site.register(publisher_model, PublisherAdmin)
admin.site.register(resourceType_model)
admin.site.register(alternateIdentifiers_model)
admin.site.register(relatedIdentifier_model)
admin.site.register(size_model)
admin.site.register(format_model)
admin.site.register(description_model)
#admin.site.register(title_model)

def autoregister(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass


#autoregister('datacite')
