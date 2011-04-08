from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_restapi.responder import *
from django_restapi.receiver import *
from schools.models import *

def KLP_addNewUser(request,template_name='viewtemplates/add_new_user.html', post_change_redirect=None):
    user = request.user     
    klp_UserGroups = user.groups.all()
    user_GroupsList = ['%s' %(usergroup.name) for usergroup in klp_UserGroups]
    if user.id is not None and (user.is_superuser or 'AdminGroup' in user_GroupsList):
        if post_change_redirect is None:
            post_change_redirect = reverse('Akshara.AkshararestApi.KLP_UserApi.KLP_addNewUser_done')
        print request.POST
        if request.method == "POST":
        
            form = UserCreationFormExtended(request.POST)
            print form
            if form.is_valid():      	       	          	    
                form.save()
                return HttpResponseRedirect(post_change_redirect)
            else:
                return render_to_response(template_name,{'form':form, 'title':'KLP User', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request)) 
        else:   	
            form = UserCreationFormExtended()
            print form
            return render_to_response(template_name,{'form':form, 'title':'KLP User', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request)) 
    else:
        return HttpResponseRedirect('/login/') 
        
def KLP_addNewUser_done(request):
    return render_to_response('viewtemplates/userAction_done.html',{'message':'User Creation Successful', 'title':'KLP User', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request))
    


def KLP_password_change(request, template_name='viewtemplates/password_change_form.html',
                    post_change_redirect=None):
    user = request.user
    usrUrl = {'Data Entry Executive':'/home/', 'Data Entry Operator':'/home/?respType=filter', 'AdminGroup':'/home/?respType=userpermissions'}
    if user.is_superuser:
    	returnUrl = '/home/'
    elif user.is_staff:
    	returnUrl = '/home/?respType=programme'
    else:
    	userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    if user.id is not None:                
        if post_change_redirect is None:
            post_change_redirect = reverse('Akshara.AkshararestApi.KLP_UserApi.KLP_password_change_done')
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_change_redirect)
            else:                                        
                return render_to_response(template_name,{'form':form, 'returnUrl':returnUrl, 'title':'KLP Change Password', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request))    
        else:
            form = PasswordChangeForm(request.user)
            return render_to_response(template_name,{'form':form, 'returnUrl':returnUrl, 'title':'KLP Change Password', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')    
        
def KLP_password_change_done(request, template_name='viewtemplates/password_change_done.html'):  
	user = request.user
	usrUrl = {'Data Entry Executive':'/home/', 'Data Entry Operator':'/home/?respType=filter', 'AdminGroup':'/home/?respType=userpermissions'}
        if user.is_superuser:
        	returnUrl = '/home/'
        elif user.is_staff:
        	returnUrl = '/home/?respType=programme'
        else:
        	userGroup = user.groups.all()[0].name
        	returnUrl = usrUrl[userGroup]
	return render_to_response(template_name,{'returnUrl':returnUrl, 'title':'KLP Change Password', 'legend':'Karnataka Learning Partnership', 'entry':"Add"},context_instance=RequestContext(request))         
    
    
    
urlpatterns = patterns('',           
   url(r'^accounts/auth/user/add/$', KLP_addNewUser),
   url(r'^accounts/auth/user/addNewUser_done/$', KLP_addNewUser_done),  
   url(r'^accounts/password/change/$', KLP_password_change),
   url(r'^accounts/password/done/$', KLP_password_change_done),
)    
