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

# This filter is used to display key value from dictionary by adding '_u' to key.
@register.filter(name='assesmentUpdation')        
def assesmentUpdation(dictionary, key):
    try:
        return dictionary[key+'_u']
    except:
        pass    
        
                    
# This filter is used to render field in edit/entry forms        
@register.inclusion_tag("render_field.html")
def render_field(field,attributes=''):

    """ render a field with its errors, optionally passing in 

        attributes eg.:  

        {% render_field form.name "cols=40,rows=5,class=text,tabindex=2" %}

        this is equivalent to

        <p>{{form.name.errors}}</p>

        {{ form.name }}



        but will also add the custom attributes

    """

    return {'errors':field.errors,'widget':make_widget(field,attributes)}
    
def make_widget(field,attributes):

    attr = {}

    if attributes:

        attrs = attributes.split(",")

        if attrs:

            for at in attrs:

                key,value = at.split("=")

                attr[key] = value

    return field.as_widget(attrs=attr)


