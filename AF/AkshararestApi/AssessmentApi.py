from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

from pysqlite2 import dbapi2 as sqlite

class AssessmentView(Collection):    
    """ To create new Assessment assessment/creator/"""
    def get_entry(self,assessment_id):        
        assessment = Assessment.objects.get(id=assessment_id)          
        return ChoiceEntry(self, assessment)   

template_assessment_view =  AssessmentView(
    queryset = Assessment.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'assessment',        
    ),
  receiver = XMLReceiver(),
)

template_assessment_edit =  AssessmentView(
    queryset = Assessment.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'edittemplates',
        template_object_name = 'assessment',        
    ),
  receiver = XMLReceiver(),
)

class AssessmentUpdate(Resource):    
    """ To update Assessment data after edit
    To update Assessment data assessment/(?P<assessment_id>\d+)/update/"""
    def create(self,request,assessment_id):         
         assessment = Assessment.objects.get(pk=assessment_id)    
         form =Assessment_Form(request.POST, request.FILES,instance=assessment)         
         form.save()    
         respTemplate= render_to_response('viewtemplates/assessment_detail.html', {'assessment':assessment})
         return HttpResponse(respTemplate)
         
         
class AssessmentStart(Resource):
    """ To start Assessment assessmentdetail/(?P<<assessment_id>\d+)/start/"""
    def read(self, request, assessment_id):
        assessObj = Assessment.objects.get(id=assessment_id)
        query = assessObj.query
        connection = sqlite.connect('/home/mahiti/Akshara/Akshara/akshara.db')
        cursor = connection.cursor()
        cursor.execute(query)
        students = cursor.fetchall()
        questions = AssessmentDetail.objects.filter(assessment=assessObj)
        counter = 0
        for student in students:
            for ques in questions:
                ansObj = Answer(assessmentDetail=ques, student_id=student[0])
                ansObj.save()
            counter +=1
        respStr =  '<div class="boundDetail" style="text-align:center;"><b>%s&nbsp;&nbsp;Started and %s Student records are updated.</b></div>' %(assessObj.name, counter)       
        return HttpResponse(respStr)
             


urlpatterns = patterns('',             
   url(r'^assessment/(?P<referKey>\d+)/creator/?$', template_assessment_view.responder.create_form, {'form_class':'assessment'}),
   url(r'^assessment/(?P<assessment_id>\d+)/view/?$', template_assessment_view),   
   url(r'^assessment/(?P<assessment_id>\d+)/edit/?$', template_assessment_edit),
   url(r'^assessment/(?P<assessment_id>\d+)/update/?$', AssessmentUpdate(permitted_methods=('POST','PUT','GET','DELETE'))),  
   url(r'^programme/(?P<referKey>\d+)/assessment/(?P<duplKey>\d+)/copy/?$', template_assessment_view.responder.create_form, {'form_class':'assessment'}), 
   url(r'^assessment/(?P<assessment_id>\d+)/start/?$', AssessmentStart(permitted_methods=('POST','PUT','GET','DELETE'))),
)
