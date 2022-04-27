import imp
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def split_timesince(value, delimiter=None):
    return value.split(delimiter)[0]


split_timesince.is_safe = True


def create_tag_link(tag):
    url = "/tags/{}".format(tag)
    return '<a href="{}">#{}</a>'.format(url, tag)


def create_profile_link(profile):
    url = "/profile/{}".format(profile)
    return '<a href="{}">@{}</a>'.format(url, profile)


@register.filter(name='hashchange')
def hashtag_links(value):

    return mark_safe(re.sub(r"#(\w+)", lambda m: create_tag_link(m.group(1)), escape(value)))


@register.filter(name='profilechange')
def profile_links(value):

    return mark_safe(re.sub(r"@(\w+)", lambda p: create_profile_link(p.group(1)), value))
