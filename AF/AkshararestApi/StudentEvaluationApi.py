from django.conf.urls.defaults import *
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry

class StudentEvaluationView(Collection):        
    def get_entry(self,question_id):        
        studentevaluation = StudentEvaluation.objects.get(id=question_id)          
        return ChoiceEntry(self, studentevaluation)   

template_studentevaluation_view =  StudentEvaluationView(
    queryset = StudentEvaluation.objects.all(),
    permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'),    
    responder = TemplateResponder(
        template_dir = 'viewtemplates',
        template_object_name = 'studentevaluation',        
    ),
  receiver = XMLReceiver(),
)


class StudentEvaluationCreate(Resource):    
    """ To create new Question question/creator/"""
    def read(self,request,referKey):            
        studentObj = student.objects.get(pk=referKey)
	questionId = request.GET['question']
	quesObj = Question.objects.get(pk=questionId)
	assessment = quesObj.assessment
	marks = request.GET['marks']
	grade = request.GET['grade']
	studEvalKey = request.GET['studEvalKey']
	if studEvalKey:
		studEvalution = StudentEvaluation.objects.get(pk=studEvalKey)
		studEvalution.marks = marks
		studEvalution.grade = grade
		studEvalution.question = quesObj
		studEvalution.save()
		respStr = quesObj.question+'&&'+str(studEvalution.id)
	else:
		studEvalution = StudentEvaluation(assessment=assessment, question=quesObj, student=studentObj, marks=marks, grade=grade)
		studEvalution.save()
		respStr = quesObj.question+'&&'+str(studEvalution.id)
        return HttpResponse(respStr)


urlpatterns = patterns('',             
   url(r'^studentEvaluation/(?P<referKey>\d+)/create/?$', StudentEvaluationCreate(permitted_methods=('POST','PUT','GET','DELETE'))),
)
