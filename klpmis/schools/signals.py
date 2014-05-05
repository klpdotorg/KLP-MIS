#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This File Contains the Signal definations. These signals 
are used to check permissions of user """

from django.dispatch import Signal

check_perm = Signal(providing_args=['user', 'instance', 'Assessment',
                    'permission'])  
                    # This Signal used to check user object level permissions

check_user_perm = Signal(providing_args=['user', 'model', 'operation'])  
# This Signal used to check user operational 
#permissions (add/update/delete permissions)

