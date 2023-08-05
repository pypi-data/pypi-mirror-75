"""
This template tag library contains tools that are used in
``floppyforms/templates/*``. We don't want to expose them publicly with
``{% load floppyforms %}``.
"""
from django import template
import ast

register = template.Library()


@register.filter
def istrue(value):
    return value is True


@register.filter
def isfalse(value):
    return value is False


@register.filter
def isnone(value):
    return value is None


def try_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


@register.filter
def isin(option, options):
    if isinstance(options, str):
        try:
            options = ast.literal_eval(options)
        except SyntaxError:
            pass
    options = [try_int(elt) for elt in options]
    try:
        option = int(option)
    except (TypeError, ValueError):
        pass
    return option in options
