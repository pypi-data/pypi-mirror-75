import logging
import re
from django import template

from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException

from webspace.loader import get_model

register = template.Library()
logger = logging.getLogger('forms')
IconSnippet = get_model('cms', 'IconSnippet')


#  Icons

@register.filter
def ico(icon, theme):
    if icon:
        if theme == 'space' or theme == 'space-inverse':
            return icon['space']
        return icon['light']
    return None


@register.filter
def ico_astro(icons, level):
    return icons['astro_level_%s' % level]


@register.filter
def ico_snippet(icon, theme):
    if not hasattr(icon, theme):
        theme = 'space'
    doc = eval('icon.%s' % theme)
    if doc:
        return doc.file.url
    return IconSnippet.DEFAULT_LINK


@register.filter
def ico_get(icons, key):
    try:
        return icons[key]
    except:
        return None


#  Utils

@register.filter
def plur(value, arg='s'):
    if ',' not in arg:
        arg = ',' + arg
    bits = arg.split(',')
    if len(bits) > 2:
        return ''
    singular_suffix, plural_suffix = bits[:2]
    try:
        return singular_suffix if float(value) <= 1 else plural_suffix
    except ValueError:  # Invalid string that's not a number.
        pass
    except TypeError:  # Value isn't a string or a number; maybe it's a list?
        try:
            return singular_suffix if len(value) <= 1 else plural_suffix
        except TypeError:  # len() of unsized object.
            pass
    return ''


@register.filter
def embed(url):
    try:
        embed = get_embed(url)
        ret = embed.html.replace('width="480"', '')
        ret = ret.replace('height="270"', '')
        ret = ret.replace('src=', 'class="lazy" data-src=')
        return ret
    except EmbedException:
        return "<iframe title='embed' class='lazy' data-src='%s'></iframe>" % url


@register.filter
def strfix(value):
    return value.replace('\n', '')


@register.filter
def klass(ob):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '-\\1', ob.__class__.__name__).lower().strip('-')


@register.filter
def cached_form(form, request):
    if form:
        if 'current_form_id' in request.session and request.session['current_form_id'] and form.id == request.session[
            'current_form_id']:
            logger.debug("Take form cached")
            return form.get_form(request.POST, request.FILES, user=request.user)
        logger.debug("Take new form")
        return form.get_form()
    logger.debug("No forms")
    return []


@register.filter
def debug(item):
    import pdb
    pdb.set_trace()
    return
