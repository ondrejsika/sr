from django import template

from ..models import GirlRank

register = template.Library()

@register.simple_tag
def rank_girl_user(girl, user):
    try:
        return GirlRank.get(girl=girl, user=user).rank
    except AttributeError:
        return '-'


@register.simple_tag
def rank(number):
    if number:
        return round(number, 2)
    return '-'
