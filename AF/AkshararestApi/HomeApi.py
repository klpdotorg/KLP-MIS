from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.template import Template, Context, RequestContext
from schools.forms import *
from django_restapi.authentication import *

class Home(Resource):
    """ To generate Home Page home/"""
    def read(self,request):
        respType = request.GET.get('respType') or None
        respDict = {'legend':'Karnataka Learning Program ', 'title':'Karnataka Learning Program ', 'entry':'Add'}
        if respType == None:
            respDict['home'] = True
        if respType == 'programme':
            respDict['programme'] = True
        if respType == 'filter':
            respDict['home'] = True    
            respDict['filter'] = True  
            respDict['prgsList'] =  Programme.objects.filter(active=1,)
        respTemplate = render_to_response("viewtemplates/home.html",respDict)
        return HttpResponse(respTemplate)
        
        
class QuestionSearch(Resource):
    """ To generate Question Search Page question/search"""
    def read(self,request):
        search_key = request.GET.get('searchtext')
        if search_key:
            questionBank = Question.objects.filter(tags__icontains=search_key)
        else:
            questionBank = Question.objects.all()
        val=Collection(questionBank, permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(paginate_by = 2, template_dir = 'viewtemplates', template_object_name = 'questions'), entry_class = ChoiceEntry, )
        
        return HttpResponse(val(request))  
        
class QuestionSearch1(Resource):
    """ To generate Question Search Page question/search"""
    def read(self,request):
        search_key = request.GET.get('searchtext')
        if search_key:
            questionBank = Question.objects.filter(tags__icontains=search_key)
        else:
            questionBank = Question.objects.all()
        val=Collection(questionBank, permitted_methods = ('GET', 'POST', 'PUT', 'DELETE'), responder = TemplateResponder(paginate_by = 2, template_dir = 'viewtemplates', template_object_name = 'questions'), entry_class = ChoiceEntry, )
        
        return HttpResponse(val(request)) 
        
         
def Testing(request):
        return HttpResponse(TestAns(permitted_methods=('POST','PUT','GET','DELETE')).read(request))
class TestAns(Resource):
    """ To Edit Answers"""
    def read(self,request):
        student_list =  request.POST.getlist('student')
        programId = request.POST['programId']
        for student in student_list:
            Ans_List = Answer.objects.filter(assessmentDetail__assessment__programme__id=programId, student__id=student)
            for ans in Ans_List:
                textField = 'student_%s_%s' %(programId, ans.id)
                textFieldVal = request.POST[textField]
                ans.answer = textFieldVal
                ans.save()
        return 'student data commited'
                
        
urlpatterns = patterns('',             
   url(r'^home/$', Home(permitted_methods=('POST','PUT','GET','DELETE'))),
   url(r'^question/search/$', QuestionSearch(permitted_methods=('POST','PUT','GET','DELETE'))),  
   
   url(r'^answer/student/edit/$',  Testing),   
)        
