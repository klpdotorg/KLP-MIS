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
from django.utils import simplejson

from schools.signals import check_user_perm
from schools.receivers import KLP_user_Perm

class KLP_Institution(Collection):    
    """ To view selected institution details
    To view selected institution boundary/(?P<boundary_id>\d+)/institution/(?P<institution_id>\d+)/view/
    To edit selected institution boundary/(?P<boundary_id>\d+)/institution/(?P<institution_id>\d+)/edit/
    To create new institution boundary/(?P<referKey>\d+)/institution/creator/"""
    def get_entry(self, institution_id):        
        institution = Institution.objects.get(id=institution_id)          
        return ChoiceEntry(self, institution)


def KLP_Institution_Create(request, referKey):
	""" To Create New Institution boundary/(?P<referKey>\d+)/institution/creator/"""
	check_user_perm.send(sender=None, user=request.user, model='Institution', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	selCategoryTyp = request.POST.get('form-0-cat')
	if selCategoryTyp:
		selCategoryTyp = int(selCategoryTyp)
	boundaryObj = Boundary.objects.get(pk=referKey)
	institutionType = 'Institution'
	categoryType = 1
	if boundaryObj.boundary_category.boundary_category.lower() == 'circle':
		institutionType = 'Anganwadi'
		categoryType = 2
	categoryList = Institution_Category.objects.filter(categoryType = categoryType)
        KLP_Create_Institution = KLP_Institution(queryset = Institution.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'institution', extra_context={'buttonType':buttonType, 'referKey':referKey, 'institutionType':institutionType, 'categoryList':categoryList, 'selCategoryTyp':selCategoryTyp}), receiver = XMLReceiver(),)
        response = KLP_Create_Institution.responder.create_form(request,form_class=Institution_Form)
        
        return HttpResponse(response)
	
	
def KLP_Institution_View(request, institution_id):
	""" To View Selected Institution institution/(?P<institution_id>\d+)/view/?$"""
	kwrg = {'is_entry':True}
	resp=KLP_Institution(queryset = Institution.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'institution',),)(request, institution_id, **kwrg)
        return HttpResponse(resp) 	


def KLP_Institution_Update(request, institution_id):
	""" To update Selected Institution institution/(?P<institution_id>\d+)/update/"""
	check_user_perm.send(sender=None, user=request.user, model='Institution', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	referKey = request.POST.get('form-0-boundary')
	selCategoryTyp = request.POST.get('form-0-cat')
	if selCategoryTyp:
		selCategoryTyp = int(selCategoryTyp)
	institutionObj = Institution.objects.get(id=institution_id)
	institutionType = 'Institution'
	categoryType = 1
	if institutionObj.boundary.boundary_category.boundary_category == 'Circle':
		institutionType = 'Anganwadi'
		categoryType = 2
	categoryList = Institution_Category.objects.filter(categoryType = categoryType)
	KLP_Edit_Institution =KLP_Institution(queryset = Institution.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'institution', extra_context={'buttonType':buttonType, 'referKey':referKey, 'institutionType':institutionType, 'categoryList':categoryList, 'selCategoryTyp':selCategoryTyp}), receiver = XMLReceiver(),)
	response = KLP_Edit_Institution.responder.update_form(request, pk=institution_id, form_class=Institution_Form)
	
	return HttpResponse(response)	

def KLP_Institution_Boundary(request, boundary_id, assessment_id):
	""" To List Institutions Under Boundary to Assign Permissions to the User """
	user = request.user
	check_user_perm.send(sender=None, user=request.user, model='Users', operation=None)
        check_user_perm.connect(KLP_user_Perm)
	users = User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'])
	#respDict['users'] = users
	boundaryObj = Boundary.objects.get(id=boundary_id)
	boundaryCat = boundaryObj.boundary_category
	studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id=assessment_id, active=2).values_list('student_group', flat=True).distinct()
	map_institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
	if boundaryCat.boundary_category.lower() == 'district':
		inst_list = Institution.objects.filter(boundary__parent__parent = boundaryObj, id__in=map_institutions_list, active=2).distinct()
	elif boundaryCat.boundary_category.lower() in [ 'block', 'project']:
		inst_list = Institution.objects.filter(boundary__parent = boundaryObj, id__in=map_institutions_list, active=2).distinct()
	else:
		inst_list = Institution.objects.filter(boundary = boundaryObj, id__in=map_institutions_list, active=2).distinct()
	val=Collection(inst_list, permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'institution', extra_context={'users':users, 'boundary':boundaryObj}), entry_class = ChoiceEntry, )
	return HttpResponse(val(request))	

urlpatterns = patterns('',    
   url(r'^boundary/(?P<referKey>\d+)/institution/creator/$', KLP_Institution_Create),
   url(r'^institution/(?P<institution_id>\d+)/view/?$', KLP_Institution_View),   
   url(r'^institution/(?P<institution_id>\d+)/update/?$', KLP_Institution_Update),
   url(r'^boundary/(?P<boundary_id>\d+)/assessment/(?P<assessment_id>\d+)/permissions/?$', KLP_Institution_Boundary),
)
