from django.forms import ModelForm
from models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminTimeWidget,AdminDateWidget
from django.utils.encoding import force_unicode
from django.conf import settings
import datetime, time

class Category_Form(ModelForm):

	class Meta:
		model = School_Category

class Language_Form(ModelForm):

	class Meta:
		model = Moi_Type

class Management_Form(ModelForm):

	class Meta:
		model = School_Management

class Section_Form(ModelForm):
	active = forms.BooleanField(initial=True, widget=forms.HiddenInput)
	class Meta:
		model = Sections

class Boundary_Form(ModelForm):

    class Meta:
	model = Boundary

class Boundary_Type_Form(ModelForm):
 
    class Meta:
        model = Boundary_Type


class School_Form(ModelForm):
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    class Meta:
	model = School

class Child_Form(ModelForm):
    
    class Meta:
	model = Child



class Class_Form(ModelForm):
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    class Meta:
	model = Class

class AcademicYear_Form(ModelForm):

    class Meta:
	model = Academic_Year


class Student_Form(ModelForm):
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)

    class Meta:
	model = student

class Programme_Form(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    
    class Meta:
        model = Programme
    
class Assessment_Form(ModelForm):
    query = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)       
    
    class Meta:
        model = Assessment
    
class Question_Form(ModelForm):
    tags = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
    class Meta:
        model = Question
        
class Answer_Form(ModelForm):

    class Meta:
        model = Answer        
        
class AssessmentDetail_Form(ModelForm):      
    active = forms.BooleanField(initial=True, widget=forms.HiddenInput)  
    class Meta:
        model = AssessmentDetail
