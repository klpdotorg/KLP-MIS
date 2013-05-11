#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KLP_UserApi is used 
1) To add new user 
2) To change password .
"""

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_restapi.responder import *
from django_restapi.receiver import *
from schools.models import *


def KLP_addNewUser(request,
                   template_name='viewtemplates/add_new_user.html',
                   post_change_redirect=None):
    """ This method uses for to create or add new user """

    user = request.user  # Get logged in user
    klp_UserGroups = user.groups.all()  # Get user groups
    user_GroupsList = ['%s' % usergroup.name for usergroup in
                       klp_UserGroups]
    if user.id is not None and (user.is_superuser or 'AdminGroup'
                                in user_GroupsList):

        # if use is login and user is super user or in admin group

        if post_change_redirect is None:
            post_change_redirect = \
                reverse('klprestApi.KLP_UserApi.KLP_addNewUser_done')
        if request.method == 'POST':

            # Get Data From Form

            form = UserCreationFormExtended(request.POST)
            if form.is_valid():

                # if form is valid save data     ....       ....          ....

                form.save()
                return HttpResponseRedirect(post_change_redirect)
            else:

                # else redirect back to add new user form

                return render_to_response(template_name, {
                    'form': form,
                    'title': 'KLP User',
                    'legend': 'Karnataka Learning Partnership',
                    'entry': 'Add',
                    }, context_instance=RequestContext(request))
        else:
            form = UserCreationFormExtended()
            return render_to_response(template_name, {
                'form': form,
                'title': 'KLP User',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add',
                }, context_instance=RequestContext(request))
    else:

        # if use is not login and user is not super user or not in admin group

        return HttpResponseRedirect('/login/')


def KLP_addNewUser_done(request):
    """ To Show User Creation done page"""

    return render_to_response('viewtemplates/userAction_done.html', {
        'message': 'User Creation Successful',
        'title': 'KLP User',
        'legend': 'Karnataka Learning Partnership',
        'entry': 'Add',
        }, context_instance=RequestContext(request))


def KLP_password_change(request,
                        template_name='viewtemplates/password_change_form.html'
                        , post_change_redirect=None):
    """ To Change Password """

    user = request.user  # Get logged in user
    usrUrl = {'Data Entry Executive': '/home/',
              'Data Entry Operator': '/home/?respType=filter',
              'AdminGroup': '/home/?respType=userpermissions'}
    if user.is_superuser:
        returnUrl = '/home/'
    elif user.is_staff:
        returnUrl = '/home/?respType=programme'
    else:
        userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    if user.id is not None:

        # if user is logged in

        if post_change_redirect is None:
            post_change_redirect = \
                reverse('production.klprestApi.KLP_UserApi.KLP_password_change_done'
                        )
        if request.method == 'POST':

            # if request method is post post data to form

            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():

                # if form is valid save data to change pwd.

                form.save()

                # redirects to password change done.

                return HttpResponseRedirect(post_change_redirect)
            else:
                return render_to_response(template_name, {
                    'form': form,
                    'returnUrl': returnUrl,
                    'title': 'KLP Change Password',
                    'legend': 'Karnataka Learning Partnership',
                    'entry': 'Add',
                    }, context_instance=RequestContext(request))
        else:
            form = PasswordChangeForm(request.user)
            return render_to_response(template_name, {
                'form': form,
                'returnUrl': returnUrl,
                'title': 'KLP Change Password',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add',
                }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def KLP_password_change_done(request,
                             template_name='viewtemplates/password_change_done.html'
                             ):
    """ To Show Password Change done page. """

    user = request.user
    usrUrl = {'Data Entry Executive': '/home/',
              'Data Entry Operator': '/home/?respType=filter',
              'AdminGroup': '/home/?respType=userpermissions'}
    if user.is_superuser:
        returnUrl = '/home/'
    elif user.is_staff:
        returnUrl = '/home/?respType=programme'
    else:
        userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    return render_to_response(template_name, {
        'returnUrl': returnUrl,
        'title': 'KLP Change Password',
        'legend': 'Karnataka Learning Partnership',
        'entry': 'Add',
        }, context_instance=RequestContext(request))


urlpatterns = patterns('', url(r'^accounts/auth/user/add/$',
                       KLP_addNewUser),
                       url(r'^accounts/auth/user/addNewUser_done/$',
                       KLP_addNewUser_done),
                       url(r'^accounts/password/change/$',
                       KLP_password_change),
                       url(r'^accounts/password/done/$',
                       KLP_password_change_done))
