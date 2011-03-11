from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.contrib.contenttypes.models import ContentType

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm

class KLP_Staff(Collection):
    """To get Paricular Staff """
    def get_entry(self, staff_id):        
        staff = Staff.objects.get(id=int(staff_id))
        return ChoiceEntry(self, staff)     
        
def KLP_Staff_View(request, staff_id):
	""" To View Selected staff staff/(?P<staff_id>\d+)/view/$"""
	kwrg = {'is_entry':True}
	resp=KLP_Boundary(queryset = Staff.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'staff',))(request, staff_id, **kwrg)
        return HttpResponse(resp)          
        
def KLP_Staff_Create(request, referKey):
	""" To Create New Staff institution/(?P<referKey>\d+)/staff/creator/"""
	check_user_perm.send(sender=None, user=request.user, model='Staff', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	url = '/institution/%s/staff/creator/' %(referKey)
	extra_dict={'buttonType':buttonType, 'referKey':referKey, 'url':url}
	extra_dict['institution_id'] =  referKey
	extra_dict['stgrps'] = StudentGroup.objects.filter(institution__id = referKey, active=2).order_by("name","section")
	institutionObj = Institution.objects.get(pk = referKey)
	if institutionObj.boundary.boundary_category.boundary_category.lower() == 'circle':
		extra_dict['institutionType'] = 'Anganwadi'
		Staff_Types = Staff_Type.objects.filter(categoryType=2)
	else:
		extra_dict['institutionType'] = 'Institution'
		Staff_Types = Staff_Type.objects.filter(categoryType=1)
	extra_dict['Staff_Types'] = Staff_Types	
        KLP_Create_Staff =KLP_Staff(queryset = Staff.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'staff', extra_context=extra_dict), receiver = XMLReceiver(),)
        
	response = KLP_Create_Staff.responder.create_form(request,form_class=Staff_Form)
	return HttpResponse(response)  


def KLP_staff_view(request, institution_id):
	""" To view list of staff in school school/(?P<school_id>\d+)/staff/view/"""
	#stdgrp_list = StudentGroup.objects.filter(content_type__model = "school", object_id=school_id)
	queryset = Staff.objects.filter(institution__id = institution_id, active=2).order_by('firstName')
	url = '/institution/%s/staff/view/' %(institution_id)
	val= Collection(queryset,
	permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),
	responder = TemplateResponder(
	paginate_by = 10,
	template_dir = 'viewtemplates',
	template_object_name = 'staff',
	extra_context = {'url':url,}
	),
	entry_class = ChoiceEntry,
	)
	return HttpResponse(val(request))
	
	
def KLP_Staff_Update(request, staff_id):
	""" To update Selected staff staff/(?P<staff_id>\d+)/update/"""
	#print '*****************************'
	check_user_perm.send(sender=None, user=request.user, model='Staff', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
        #print 1111111111111111111111
	buttonType = request.POST.get('form-buttonType')
	referKey = request.POST.get('form-0-boundary')
	staff = Staff.objects.get(pk=staff_id)
	stgrps = StudentGroup.objects.filter(institution = staff.institution, active=2)
	institutionObj = staff.institution
	if institutionObj.boundary.boundary_category.boundary_category.lower() == 'circle':
		institutionType = 'Anganwadi'
		Staff_Types = Staff_Type.objects.filter(categoryType=2)
	else:
		institutionType = 'Institution'
		Staff_Types = Staff_Type.objects.filter(categoryType=1)
	#print 'aaaaaaaaaaaaaaaaaa'
	KLP_Edit_Staff =KLP_Staff(queryset = Staff.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'staff', extra_context={'buttonType':buttonType, 'referKey':referKey, 'stgrps':stgrps, 'institutionType':institutionType, 'Staff_Types':Staff_Types}), receiver = XMLReceiver(),)
	#print 'bbbbbbbbbbbbbbbbbb'
	response = KLP_Edit_Staff.responder.update_form(request, pk=staff_id, form_class=Staff_Form)
	#print 'sssssssssssssssssssssssss'
	return HttpResponse(response)		
			      

urlpatterns = patterns('',
   url(r'^staff/(?P<staff_id>\d+)/view/$', KLP_Staff_View),
   url(r'institution/(?P<referKey>\d+)/staff/creator/?$', KLP_Staff_Create),
   url(r'^institution/(?P<institution_id>\d+)/staff/view/$', KLP_staff_view),
   url(r'^staff/(?P<staff_id>\d+)/update/$', KLP_Staff_Update),
   
)	
