from schools.models import *
from schools.forms import *
from django import template
from django.http import HttpResponse
from django.shortcuts import render_to_response
register = template.Library()


@register.filter(name='getAssessmentQuestions')
def getAssessmentQuestions(obj, resp): 
    try:
        AssessDetail_list = AssessmentDetail.objects.filter(assessment=obj)
        if resp == 'length':
            return len(AssessDetail_list)
        else: 
            return AssessDetail_list
    except:        
        pass      
        
@register.filter(name='getAnswers')        
def getAnswers(obj, student):
    try:
        ans_list = Answer.objects.filter(assessmentDetail__assessment=obj, student=student)
        return ans_list
    except:
        pass          
        
@register.filter(name='getAssessments')        
def getAssessments(filter_id):
    try:
        Assessment_list = Assessment.objects.filter(programme__id=filter_id) 
        return Assessment_list    
    except:
        pass
        

