from django.http import HttpResponse, Http404
from django.template import Context, loader
from datacite.models import resource_model


def index(request):
    resources = resource_model.objects.all()
    t = loader.get_template('index.html')
    c = Context({'object_list': resources})
    return HttpResponse(t.render(c))

def queue(request):
    resources = resource_model.objects.all()
    t = loader.get_template('queue.html')
    c = Context({'object_list': resources})
    return HttpResponse(t.render(c))

def detail(request, slug):
    try:
        resource = resource_model.objects.get(slug=slug)
    except resource_model.DoesNotExist:
        raise Http404
    t = loader.get_template('detail.html')
    c = Context({'object': resource})
    return HttpResponse(t.render(c))

def xml(request, slug, disposition=None):
    try:
        resource = resource_model.objects.get(slug=slug)
    except resource_model.DoesNotExist:
        raise Http404
    if('send' == disposition):
        return HttpResponse("Unimplemented")
    t = loader.get_template('metadata.xml')
    c = Context({'object': resource})
    response = HttpResponse(t.render(c), content_type="text/xml")
    if('download' == disposition):
        response['Content-Disposition'] = 'attachment; filename=metadata.xml'
    return response
