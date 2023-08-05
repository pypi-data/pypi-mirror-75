from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings

from webspace.loader import get_model

IconSnippet = get_model('cms', 'IconSnippet')


def robots(request):
    return HttpResponse(
        render_to_string('robots.txt', {'request': request}),
        content_type='text/plain'
    )


def error_404(request, exception):
    context = {}
    context['icons'] = IconSnippet.get_context()
    return render(request, 'cms/pages/404.html', context, status=404)


def worker(request):
    from wagtail.contrib.sitemaps.sitemap_generator import Sitemap
    return HttpResponse(render_to_string(
        'worker.js',
        {
            'request': request,
            'pages': Sitemap(request),
            'version': settings.VERSION_WEBSPACE
        }),
        content_type='application/javascript'
    )
