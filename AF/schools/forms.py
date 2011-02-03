from django.forms import ModelForm
from models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminTimeWidget,AdminDateWidget
from django.utils.encoding import force_unicode
from django.conf import settings
import datetime, time
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import *


class Institution_Category_Form(ModelForm):

	class Meta:
		model = Institution_Category

class Moi_Type_Form(ModelForm):

	class Meta:
		model = Moi_Type

class Institution_Management_Form(ModelForm):
	name = forms.CharField(max_length = 50, required=True)
	class Meta:
		model = Institution_Management


class Boundary_Form(ModelForm):
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
	model = Boundary

class Boundary_Type_Form(ModelForm):
 
    class Meta:
        model = Boundary_Type


class Institution_address_Form(ModelForm):
	address = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}))
	area = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}), required=False)
	pincode = forms.CharField(required=False)
	landmark = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':20}), required=False)
	instidentification = forms.CharField(required=False)
	routeInformation = forms.CharField(required=False)
	class Meta:
		model = Institution_address

class Institution_Form(Institution_address_Form):
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
	model = Institution
	

class Relations_Form(ModelForm):
	first_name = forms.CharField(required=False)
	middle_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	class Meta:
		model = Relations

class Child_Form(Relations_Form):
    thisyear = datetime.date.today().year
    startyear = thisyear-20
    dob=forms.DateField( widget=SelectDateWidget(years=range(startyear,thisyear+1),attrs={'tabindex':3}))
    class Meta:
	model = Child


class StudentGroup_Form(ModelForm):
    
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
	model = StudentGroup
	

class AcademicYear_Form(ModelForm):

    class Meta:
	model = Academic_Year


class Student_Form(ModelForm):
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    class Meta:
	model = Student
	
class Staff_Form(ModelForm):
    thisyear = datetime.date.today().year
    startyear = thisyear-40
    doj=forms.DateField( widget=SelectDateWidget(years=range(startyear,thisyear+1),attrs={'tabindex':5}),required=False)	
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
	model = Staff	

class Programme_Form(ModelForm):
    startDate = forms.DateField( widget=forms.DateInput(format='%d-%m-%Y'),initial = datetime.date.today, input_formats=['%d-%m-%Y', '%d-%m-%y'])
    endDate = forms.DateField( widget=forms.DateInput(format='%d-%m-%Y'),initial = default_end_date, input_formats=['%d-%m-%Y', '%d-%m-%y'])
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    
    class Meta:
        model = Programme
    
class Assessment_Form(ModelForm):
    startDate = forms.DateField( widget=forms.DateInput(format='%d-%m-%Y'),initial = datetime.date.today, input_formats=['%d-%m-%Y', '%d-%m-%y'])
    endDate = forms.DateField( widget=forms.DateInput(format='%d-%m-%Y'),initial = default_end_date, input_formats=['%d-%m-%Y', '%d-%m-%y'])	
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)       
    
    class Meta:
        model = Assessment
    
class Question_Form(ModelForm):
    questionType = forms.ChoiceField(choices=QuestionType,)	
    scoreMin = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    scoreMax = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    grade = forms.CharField(required=False)
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput) 
    
    def clean_scoreMin(self):
        questionType = self.cleaned_data['questionType']
        scoreMin = self.cleaned_data.get('scoreMin', '')
        if questionType  == '1':
        	if not scoreMin:
            		raise forms.ValidationError("This field is required.")
            	else:
            		scoreMax = self.cleaned_data.get('scoreMax', '')
            		if scoreMin > scoreMax:
            			raise forms.ValidationError("Score Min Should be Less than Score Min.")
        return scoreMin
        
    def clean_scoreMax(self):
        questionType = self.cleaned_data['questionType']
        scoreMax = self.cleaned_data.get('scoreMax', '')
        if questionType  == '1':
        	if not scoreMax:
            		raise forms.ValidationError("This field is required.")
            	else:
            		scoreMin = self.cleaned_data.get('scoreMin', '')
            		if scoreMin > scoreMax:
            			raise forms.ValidationError("Score Max Should be Grater than Score Min.")
        return scoreMax
    
    def clean_grade(self):
        questionType = self.cleaned_data['questionType']
        grade = self.cleaned_data.get('grade', '')
        if questionType  == '2':
        	if not grade:
            		raise forms.ValidationError("This field is required.")
            	
        return grade
 
    
    class Meta:
        model = Question
        
class Answer_Form(ModelForm):

    class Meta:
        model = Answer        
        


class UserCreationFormExtended(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, 
**kwargs) 
	self.fields['groups'].required = True 

    def save(self, commit=True):
        user = super(UserCreationFormExtended, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            user.groups = (self.cleaned_data["groups"])
            user.save()
        return user
        
    class Meta: 
        model = User 
        fields = ('username', 'password1', 'password2', 'groups') 
