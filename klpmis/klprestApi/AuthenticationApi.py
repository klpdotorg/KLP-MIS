#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
AuthenticationApi is used 
1) To login
2) To logout
3) To check user is logged in or not.
"""

from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from klprestApi.BoundaryApi import ChoiceEntry
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
#from django.views.generic.simple import *
class Redirect_View(TemplateView):
    template_name = "login.html"

def KLP_Login(request):
    """ This method is for user login """

    user = request.user
    if request.method == 'POST':

    # check method is post

        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

    # check user is logged in

        if user is not None:

      # If user not logged in check user is active user

            if user.is_active:
                login(request, user)

        # success

                usrUrl = {'Data Entry Executive': '/home/',
                          'Data Entry Operator': '/home/?respType=filter',
                          'AdminGroup': '/home/?respType=userpermissions'}
                if user.is_superuser or user.is_staff:

            # If user is super user or staff redirect to home page after login.

                    return HttpResponseRedirect('/home/')
                else:

            # else redirect to respective paths defined in usrUrl dictionary based on group.

                    userGroup = user.groups.all().defer('user',
                            'permissions')[0].name
                    return HttpResponseRedirect(usrUrl[userGroup])
            else:

        # disabled account

                return render_to_response( 'login.html', {
                    'message': 'Please enter a correct username and password'
                        ,
                    'title': 'Karnataka Learning Partnership',
                    'legend': 'Karnataka Learning Partnership',
                    'entry': 'Add',
                    }, context_instance=RequestContext(request))
        else:

            # invalid login
            
            return render_to_response('login.html',
            {
                'message': 'Please enter a correct username and password'
                    ,
                'title': 'Karnataka Learning Partnership',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add',
                }, context_instance=RequestContext(request))
            
            #return Redirect_View.as_view() 
            ''',extra_context={
                'message': 'Please enter a correct username and password'
                    ,
                'title': 'Karnataka Learning Partnership',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add',
                })
            '''

    else:
        return render_to_response('login.html', {
            'user': user,
            'title': 'Karnataka Learning Partnership',
            'legend': 'Karnataka Learning Partnership',
            'entry': 'Add',
            }, context_instance=RequestContext(request))


def KLP_Logout_user(request):
    """ This method is for user logout """

    logout(request)
    return render_to_response('login.html',
                              {'title': 'Karnataka Learning Partnership'
                              ,
                              'legend': 'Karnataka Learning Partnership'
                              , 'entry': 'Add'},
                              context_instance=RequestContext(request))


def KLP_User_Auth(request):
    """ This method checks, user is authenticated or not """

    return HttpResponse(request.user.is_authenticated())


urlpatterns = patterns('', url(r'^login/?$', KLP_Login),
                       url(r'^logout/?$', KLP_Logout_user),
                       url(r'^user/authentication/?$', KLP_User_Auth))
