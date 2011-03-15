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

class KLP_StudentGroup(Collection):    
    """ To view selected Class details
    To view selected Class boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/view/
    To edit selected Class boundary/(?P<boundary_id>\d+)/schools/(?P<school_id>\d+)/edit/
    To Create New StudentGroup boundary/(?P<bounday>\d+)/schools/(?P<school>\d+)/class/creator/"""
    def get_entry(self, studentgroup_id):        
        StudentGroups = StudentGroup.objects.get(id=studentgroup_id)          
        return ChoiceEntry(self,StudentGroups )

def KLP_StudentGroup_Create(request, referKey):
	""" To Create New StudentGroup boundary/(?P<bounday>\d+)/schools/(?P<school>\d+)/class/creator/"""
	check_user_perm.send(sender=None, user=request.user, model='StudentGroup', operation='Add')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	instObj = Institution.objects.get(id = referKey)
	group_typ = request.GET.get("group_typ") or request.POST.get("group_typ")
        KLP_Create_StudentGroup = KLP_StudentGroup(queryset = StudentGroup.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'studentgroup', extra_context={'buttonType':buttonType, 'ParentKey':referKey, 'group_typ':group_typ, 'sch_typ':instObj.boundary.boundary_category.boundary_category}), receiver = XMLReceiver(),)
        response = KLP_Create_StudentGroup.responder.create_form(request,form_class=StudentGroup_Form)
        return HttpResponse(response)
	
	
def KLP_StudentGroup_View(request, studentgroup_id):
	""" To View Selected StudentGroup studentsroup/(?P<studentsroup_id>\d+)/view/?$"""
	reqlist= request.GET.items()
	itemlist=[str(k[0]) for k in reqlist]
	if 'count' in itemlist:
		count = request.GET['count']
	else:
		count = '0'
	kwrg = {'is_entry':True}
	studentgroup = StudentGroup.objects.get(id=studentgroup_id)
	url = '/studentgroup/'+studentgroup_id+'/view/'
	school = Institution.objects.get(id = studentgroup.institution.id)
	studgrpParent = school
	studentGroups = StudentGroup.objects.filter(institution__id=studgrpParent.id,group_type="Center", active=2)
	
	Norecords = len(Student_StudentGroupRelation.objects.filter(student_group__id = studentgroup_id,academic=current_academic, active=2))
	students = Student_StudentGroupRelation.objects.filter(student_group__id = studentgroup_id, academic=current_academic, active=2, student__active=2).order_by('student__child__firstName')
	resp=Collection(students, permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'viewtemplates', template_object_name = 'students',paginate_by = 20,extra_context={'studgrpParent':studgrpParent,'studentgroup':studentgroup,'url':url, 'students':students,'Norecords':Norecords, 'studentGroups':studentGroups,'count':count}),)
        return HttpResponse(resp(request))

def KLP_StudentGroup_Update(request, studentgroup_id):
	""" To update Selected School school/(?P<school_id>\d+)/update/"""
	check_user_perm.send(sender=None, user=request.user, model='StudentGroup', operation='Update')
        check_user_perm.connect(KLP_user_Perm)
	buttonType = request.POST.get('form-buttonType')
	ParentKey = request.POST.get('form-0-institution')
	group_typ = request.GET.get("group_typ") or request.POST.get("group_typ")
	sgObj = StudentGroup.objects.get(pk=studentgroup_id)
	sch_typ = request.GET.get("sch_typ") or sgObj.institution.boundary.boundary_category
	KLP_Edit_StudentGroup =KLP_StudentGroup(queryset = StudentGroup.objects.all(), permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'edittemplates', template_object_name = 'studentgroup', extra_context={'buttonType':buttonType,'ParentKey':ParentKey, 'group_typ':group_typ, 'sch_typ':sch_typ}), receiver = XMLReceiver(),)
	response = KLP_Edit_StudentGroup.responder.update_form(request, pk=studentgroup_id, form_class=StudentGroup_Form)
	return HttpResponse(response)	

def KLP_StudentGroup_Answer_Entry(request, studentgroup_id, programme_id, assessment_id):
	""" To Show Answer Entry Form studentgroup/(?P<studentgroup_id>\d+)/programme/(?P<programme_id>\d+)/assessment/(?P<assessment_id>\d+)/view/"""
	user = request.user
	#canEnter = user.has_perm('schools.change_answer')
	canEnter = True
	url = "/studentgroup/%s/programme/%s/assessment/%s/view/" %(studentgroup_id, programme_id, assessment_id)
	if canEnter:
		students = Student_StudentGroupRelation.objects.filter(student_group__id = studentgroup_id, academic=current_academic, active=2).values_list('student__child', flat=True).distinct()
		grupObj = StudentGroup.objects.get(pk = studentgroup_id)
		students_list = Student.objects.filter(id__in = students, active=2,).order_by("child__firstName").distinct()
		students_list = Child.objects.filter(id__in=students)
		assessmentObj = Assessment.objects.get(pk=assessment_id)
		val=Collection(students_list, permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(template_dir = 'prgtemplates', template_object_name = 'students', paginate_by=20, extra_context={'filter_id':programme_id, 'assessmentObj':assessmentObj, 'user':user, 'studentgroup_id':studentgroup_id, 'group_typ':grupObj.group_type, 'url':url}), entry_class = ChoiceEntry, )
		return HttpResponse(val(request))
	else:
		return HttpResponse("<b><font color='red'>Insufficient Priviliges to Access This Data</font></b>")	

def MapStudents(request,id):
	student_id = request.POST.getlist('students')
	count = 0
	if request.POST['StdgrpCtr'] == 'None':
		studentgroup_id = ''
	else:
		studentgroup_id = request.POST['StdgrpCtr']
	if student_id and studentgroup_id:
		studentgroup =  StudentGroup.objects.get(pk = studentgroup_id)
		school =  Institution.objects.get(pk = request.POST['school'])
		academic =  Academic_Year.objects.get(pk = current_academic().id)
		for student in student_id:
			student = Student.objects.get(pk = student)
			param={'id':None,'student':student,'student_group':studentgroup,'academic':academic,'active':2}
			stdgrp_rels = Student_StudentGroupRelation.objects.get_or_create(**param)
			count = count+1
	return HttpResponseRedirect('/studentgroup/'+str(id)+'/view/?count='+str(count))

urlpatterns = patterns('',    
   url(r'^boundary/institution/(?P<referKey>.*)/studentgroup/creator/$', KLP_StudentGroup_Create),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/view/?$', KLP_StudentGroup_View),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/update/?$', KLP_StudentGroup_Update),
   url(r'^studentgroup/(?P<studentgroup_id>\d+)/programme/(?P<programme_id>\d+)/assessment/(?P<assessment_id>\d+)/view/?$', KLP_StudentGroup_Answer_Entry),
   url(r'^mapstudents/(?P<id>\d+)/$', MapStudents),
)
