#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import dispatch

post_create = dispatch.Signal()
post_adjust = dispatch.Signal()

