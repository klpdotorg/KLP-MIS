#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This file contains user defined template tags to used templates to render values
"""

from schools.models import *
from schools.forms import *
from django import template
from django.http import HttpResponse
from django.shortcuts import render_to_response
register = template.Library()


# This filter is used for to return range value for pagination

@register.filter
def KLPrange(value):
    return range(value)


# This filter is used to display key value from dictionary

@register.filter(name='displayValue')
def displayValue(dictionary, key):
    try:
        return dictionary[key]
    except:

        pass


@register.filter(name='split')
def splitfirst(value, arg):
    return value.split(arg)[0]


@register.filter(name='split')
def splitsecond(value, arg):
    return value.split(arg)[1]


@register.filter(name='CatString')
def CatString(value, value1):

    return str(value) + '_' + str(value1)


@register.filter(name='dictValue')
def dictValue(dictionary, key):
    try:
        return dictionary[key]
    except:
        return ''


# This filter is used to display key value from dictionary by adding '_u' to key.

@register.filter(name='assesmentUpdation')
def assesmentUpdation(dictionary, key):
    try:
        return dictionary[key + '_u']
    except:
        pass


# This filter is used to render field in edit/entry forms

@register.inclusion_tag('render_field.html')
def render_field(field, attributes=''):
    """ render a field with its errors, optionally passing in 

        attributes eg.:  

        {% render_field form.name "cols=40,rows=5,class=text,tabindex=2" %}

        this is equivalent to

        <p>{{form.name.errors}}</p>

        {{ form.name }}



        but will also add the custom attributes

    """

    return {'errors': field.errors, 'widget': make_widget(field,
            attributes)}


def make_widget(field, attributes):

    attr = {}

    if attributes:

        attrs = attributes.split(',')

        if attrs:

            for at in attrs:

                (key, value) = at.split('=')

                attr[key] = value

    return field.as_widget(attrs=attr)


