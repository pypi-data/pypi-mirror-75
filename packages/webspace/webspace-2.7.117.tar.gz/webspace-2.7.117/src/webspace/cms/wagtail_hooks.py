import re
from django.urls import include, path, reverse
from wagtail.admin.rich_text.converters import html_to_contentstate
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler, KEEP_WHITESPACE, WHITESPACE_RE
)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from webspace.bakery import urls as urls_bakery

NOTHING_RE = re.compile('a^')


#  RichText Mark

@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    feature_name = 'mark'
    type_ = 'MARK'
    tag = 'mark'

    control = {
        'type': type_,
        'label': '☆',
        'description': 'Mark',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    features.default_features.append('mark')


#  RichText Code Blocks

class PreformattedTextElementHandler(BlockElementHandler):
    """
    BlockElementHandler that preserves all whitespace.
    """

    def handle_starttag(self, name, attrs, state, contentstate):
        super().handle_starttag(name, attrs, state, contentstate)
        # Keep all whitespace while rendering this block
        html_to_contentstate.WHITESPACE_RE = NOTHING_RE
        state.leading_whitespace = KEEP_WHITESPACE

    def handle_endtag(self, name, state, contentstate):
        # Reset whitespace handling to normal behaviour
        html_to_contentstate.WHITESPACE_RE = WHITESPACE_RE
        super().handle_endtag(name, state, contentstate)


@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    feature_name = 'code-block'
    feature_type = 'code-block'
    control = {
        'type': feature_type,
        'label': '{}',
        'description': 'Code',
    }
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            'pre': PreformattedTextElementHandler(feature_type),
        },
        'to_database_format': {
            'block_map': {
                feature_type: {
                    'element': 'pre',
                    'props': {'class': 'code'},
                },
            },
        },
    })
    features.default_features.append(feature_name)


#  RichText Eternal Links

from django.utils.html import escape
from wagtail.core.rich_text import LinkHandler


class NoFollowExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]

        # Transform `rel` and `target` attribute

        target = ''
        if '/target_blank' in href:
            target = 'target="_blank"'
            href = href.replace('/target_blank', '')

        rel = 'rel="nofollow"'
        if '/rel_follow' in href:
            rel = ''
            href = href.replace('/rel_follow', '')

        return '<a href="%s" %s %s>' % (escape(href), rel, target)


@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NoFollowExternalLinkHandler)
