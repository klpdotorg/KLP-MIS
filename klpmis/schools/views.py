#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.

from django.db import models
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.context_processors import csrf

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext

from models import *
from forms import *

