#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminTimeWidget, \
    AdminDateWidget
from django.utils.encoding import force_unicode
from django.conf import settings
import datetime
import time
from django.forms.models import modelformset_factory
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import *
import psycopg2
from emsproduction.settings import *
from fullhistory.models import *
from schools.models import current_academic
d = DATABASES['default']
datebase = d['NAME']
user = d['USER']
password = d['PASSWORD']

from django.db import models
def storeFullhistory(requestparam,data,objid,modelName,action='C'):
    
    
    userid=requestparam.get('userid','user')
    username=requestparam.get('username','username')
    request_path=requestparam.get('request_path','/')
    #userid = username.id
     
    fullrequest = Request(user_name=username, user_pk=userid,
                          request_path=request_path)
    fullrequest.save()
    
    
    obj = ContentType.objects.get(model=modelName)

    content_type_id = obj.id
    
    create_info = create_infos(requestparam, action)
    
    
    try:
        revision = len(FullHistory.objects.filter(content_type=modelName,
                       object_id=objid))

    except:
        revision = 0
    revision=0 if revision==0 else  revision+1 
    fh = FullHistory(
        revision=revision,
        action=action,
        content_type_id=content_type_id,
        object_id=objid,
        data=data,
        request=fullrequest,
        site_id=1,
        info=create_info,
        )
    fh.save()
    return 'Sccess' 

def create_infos(requestparam, action):
    '''
        Generates a summary description of this history entry
        '''

    user_name = u'(System)'
    if requestparam and type(requestparam)()!={}:
        user_name = requestparam.user
    else:
       user_name=userid=requestparam.get('current_user','user')
       
    ret = {'C': u'%s Created', 'U': u'%s Updated',
           'D': u'%s Deleted'}[action] % user_name

    
    return ret
def CustomizeSave(selfObj,Form,commit=True,modelName=None):
          
          try:
                instance = super(Form, selfObj).save(commit=commit)
                
                instance.save()

                selfObj.instance=instance
          except:
              initalName=modelName
              
              modelName=Form.Meta.model._meta.module_name
              
              connection = psycopg2.connect(database=datebase, user=user,                    password=password)
              cursor = connection.cursor()
              Query="SELECT  column_default from information_schema.columns where table_name='schools_"+modelName+"' and column_name='id'"
              cursor.execute(Query)
              Seqcolumn=cursor.fetchone()[0]
              cursor.execute("select "+Seqcolumn)
              insertedRow=cursor.fetchone()[0]-1
              cursor.close()
              
              #print  selfObj.instances,'INSTANCE OBJ',selfObj.instances.id,insertedRow
              #print dir(selfObj)
              try:
                  selfObj.instance=Form.Meta.model.objects.get(id=insertedRow)
              except:
                  pass
              userdetails={}
              selfObjfiles=selfObj.files
	      try:
      			 username = selfObjfiles.user
       			 userid=username.id
                         request_path=selfObjfiles.path_info
              except:
                      userid=selfObjfiles.get('form-0-current_user','')
                      username=selfObjfiles.get('form-0-username','')
                      request_path=selfObjfiles.get('form-0-path_info','/')
              userdetails['username']=username
              userdetails['userid']=userid
              userdetails['request_path']=request_path
              if username :

                  v=storeFullhistory(userdetails,selfObj.data,insertedRow,modelName)
          return selfObj.instance

class Institution_Category_Form(ModelForm):

    class Meta:

        model = Institution_Category


class Moi_Type_Form(ModelForm):

    class Meta:

        model = Moi_Type


class Institution_Management_Form(ModelForm):

    name = forms.CharField(max_length=50, required=True)

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

    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4,
                              'cols': 20}))
    area = forms.CharField(widget=forms.Textarea(attrs={'rows': 4,
                           'cols': 20}), required=False)
    pincode = forms.CharField(required=False)
    landmark = forms.CharField(widget=forms.Textarea(attrs={'rows': 4,
                               'cols': 20}), required=False)
    instidentification = forms.CharField(required=False)
    route_information = forms.CharField(required=False)

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
    def save(self, commit=True):
          return CustomizeSave(self,Relations_Form)

    class Meta:

        model = Relations


class Child_Form(Relations_Form):
    first_name = forms.CharField(required=False)
    #middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    motherfirstname=forms.CharField(required=False)
    fatherfirstname=forms.CharField(required=False)
    motherlastname=forms.CharField(required=False)
    fatherlastname=forms.CharField(required=False)
    mothermiddlename=forms.CharField(required=False)
    fathermiddlename=forms.CharField(required=False)
    otherId=forms.CharField(required=False)
    ModelName=forms.CharField(required=False)
    thisyear = datetime.date.today().year
    startyear = thisyear - 20
    dob = \
        forms.DateField(widget=SelectDateWidget(years=range(startyear,
                        thisyear + 1), attrs={'tabindex': 1}))
    '''
    def __init__(self,  *args, **kwargs):
         #self.args=args
         self.kwargs=kwargs
         super(Child_Form, self).__init__(*args, **kwargs)
    '''
    def clean(self):
                cleaned_data = self.cleaned_data

                first_name = cleaned_data.get("first_name").strip()
                last_name = cleaned_data.get("last_name").strip()
                if not first_name:
                      msg = u"Enter First Name "
                      self._errors["first_name"] = self.error_class([msg])
                      del cleaned_data["first_name"]
                      del cleaned_data["last_name"]
                first_name = cleaned_data.get("motherfirstname").strip()
                last_name = cleaned_data.get("fatherfirstname").strip()
                if not first_name and not last_name:
                      msg = u"Enter Mother Name or Father Name"
                      self._errors["fatherfirstname"] = self.error_class([msg])
                      del cleaned_data["motherfirstname"]
                      del cleaned_data["fatherfirstname"]

                return cleaned_data
    
    def save(self, commit=True):
          print self.errors ,'ERRRRRRRRRRRRRR'           
          childObj=CustomizeSave(self,Child_Form)
          #print self.files,'kwars' ,self.instance.id,dir(self.instance)
          relationdatarequest=self.files
          childpostid=self.cleaned_data.get('id','')
          relationlist = ['father','mother'] #{'motherfirstname': 'Mother', 'fatherfirstname': 'father'}
          for  rel_value in relationlist:
                        relationobj=Relations.objects.filter(relation_type=rel_value.capitalize(),child=childObj).defer('child')
                        relationForm= modelformset_factory(relationobj.model,form=Relations_Form)
                        relationdata=relationdatarequest.POST.copy()
                        try:
                            del relationdata['form-0-id']
                        except:
                                pass

                        if self.cleaned_data[rel_value+'firstname']:

                        	relationdata['form-0-first_name']=self.cleaned_data[rel_value+'firstname']
                        	relationdata['form-0-last_name']=self.cleaned_data[rel_value+'lastname']
                        	relationdata['form-0-middle_name']=self.cleaned_data[rel_value+'middlename']
                        	relationdata['form-0-relation_type']=rel_value.capitalize()
                                relationdata['form-0-child']=childObj.id
                                if relationobj:
                                    relationdata['form-INITIAL_FORMS']=1
                                    relationdata['form-0-id']=relationobj[0].id
                                    relationdatarequest.POST=relationdata
                                    rform = relationForm(relationdata,relationdatarequest,queryset=relationobj)
                                else:
                                   relationdata['form-INITIAL_FORMS']=0
                                   relationdatarequest.POST=relationdata
                                   rform = relationForm(relationdata,relationdatarequest)

                                rform.save()
                            
                        else:

                             if relationobj:
                                   relationobj.delete()
             
          if self.cleaned_data['ModelName']=='student' and childpostid is None :
              # Create Student Object With as foreign key

	      studentForm= modelformset_factory(Student,form=Student_Form)	
              relationdata['form-0-other_student_id']=self.cleaned_data['otherId']
              relationdata['form-0-child']= childObj.id   
              try:
                        studObj = childObj.getStudent()
                        relationdata['form-0-id']=studObj.id
                        #studObj.other_student_id = \
                        #self.cleaned_data['otherId']
              except:
                       
                 pass  
                 #studObj = Student(child=self.instance,
                 #                   other_student_id=self.cleaned_data['otherId'], active=2)
              Studform = studentForm(relationdata,relationdatarequest)
              studObj=Studform.save()
              
              # Create relation ship with SG for current academic year.
              studentgroupForm= modelformset_factory(Student_StudentGroupRelation,form=Student_StudentGroupRelation_Form)
              relationdata['form-0-student_group']=relationdatarequest.POST.get('studentgroup')
              relationdata['form-0-student']=studObj[0].id
              relationdata['form-0-academic']=current_academic().id

              studgrprelation=studentgroupForm(relationdata,relationdatarequest)

              studgrprelation.save()
 
          return self.instance
    
    class Meta:

        model = Child


class StudentGroup_Form(ModelForm):

    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    class Meta:

        model = StudentGroup
    def __init__(self,  *args, **kwargs):
         #self.args=args
         self.kwargs=kwargs
         super(StudentGroup_Form, self).__init__(*args, **kwargs)
    def save(self,commit=True):
          return CustomizeSave(self,StudentGroup_Form)
          '''    
          try:
            instance = super(StudentGroup_Form, self).save(commit=commit)
            
            instance.save()
            
            return instance 
          except:
            
            if self.cleaned_data.get('id','') is None:
              connection = psycopg2.connect(database=datebase, user=user,                    password=password)
              tableactive=self.cleaned_data.get('active',2)
              cursor = connection.cursor() 
              Query="SELECT  column_default from information_schema.columns where table_name='schools_studentgroup' and column_name='id'"
              cursor.execute(Query)
              Seqcolumn=cursor.fetchone()[0]
              cursor.execute("select "+Seqcolumn) 
              insertedRow=cursor.fetchone()[0]-1
              cursor.close()
              createdObj=StudentGroup.objects.filter(id=insertedRow)
              modelName=createdObj.model._meta.module_name
              v=storeFullhistory(self.kwargs.get('files','nothing'),self.data,insertedRow,modelName)
              print createdObj,'CrateObj' 
              return createdObj
          '''
class AcademicYear_Form(ModelForm):

    class Meta:

        model = Academic_Year


class Student_Form(ModelForm):

    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    class Meta:

        model = Student
    def __init__(self,  *args, **kwargs):
         #self.args=args
         self.kwargs=kwargs
         super(Student_Form, self).__init__(*args, **kwargs)
    def save(self,commit=True):
          return CustomizeSave(self,Student_Form)
class Student_StudentGroupRelation_Form(ModelForm):

    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    class Meta:

        model = Student_StudentGroupRelation
    def __init__(self,  *args, **kwargs):
         #self.args=args
         self.kwargs=kwargs
         super(Student_StudentGroupRelation_Form, self).__init__(*args, **kwargs)
    def save(self,commit=True):
          return CustomizeSave(self,Student_StudentGroupRelation_Form)
         


class Staff_Form(ModelForm):

    thisyear = datetime.date.today().year
    startyear = thisyear - 40
    doj = \
        forms.DateField(widget=SelectDateWidget(years=range(startyear,
                        thisyear + 1), attrs={'tabindex': 5}),
                        required=False)
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    class Meta:

        model = Staff


class Programme_Form(ModelForm):

    start_date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'
                                ), initial=datetime.date.today,
                                input_formats=['%d-%m-%Y', '%d-%m-%y'])
    end_date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'
                              ), initial=default_end_date,
                              input_formats=['%d-%m-%Y', '%d-%m-%y'])
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    def clean(self):
                cleaned_data = self.cleaned_data
                start_date = cleaned_data.get("start_date")
                end_date = cleaned_data.get("end_date")
                if end_date < start_date:
                      msg = u"End date should be greater than start date."
                      self._errors["end_date"] = self.error_class([msg])
                      del cleaned_data["start_date"]
                      del cleaned_data["end_date"]
                return cleaned_data

    class Meta:

        model = Programme


class Assessment_Form(ModelForm):

    start_date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'
                                ), initial=datetime.date.today,
                                input_formats=['%d-%m-%Y', '%d-%m-%y'])
    end_date = forms.DateField(widget=forms.DateInput(format='%d-%m-%Y'
                              ), initial=default_end_date,
                              input_formats=['%d-%m-%Y', '%d-%m-%y'])
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    # flexi_assessment = forms.BooleanField(initial=False)

    primary_field_name = forms.CharField(required=False)

    # primary_field_type = forms.CharField(required=False)
    # typ = forms.IntegerField(initial=3, widget=forms.HiddenInput)
    # double_entry = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    def clean(self):
                cleaned_data = self.cleaned_data
                start_date = cleaned_data.get("start_date")
                end_date = cleaned_data.get("end_date")
                if end_date < start_date:
                      msg = u"End date should be greater than start date."
                      self._errors["end_date"] = self.error_class([msg])
                      del cleaned_data["start_date"]
                      del cleaned_data["end_date"]
                return cleaned_data

    class Meta:

        model = Assessment


class Assessment_Lookup_Form(ModelForm):

    name = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:

        model = Assessment


class Question_Form(ModelForm):

    question_type = forms.ChoiceField(choices=QuestionType)
    score_min = forms.DecimalField(max_digits=10, decimal_places=2,
                                  required=False)
    score_max = forms.DecimalField(max_digits=10, decimal_places=2,
                                  required=False)
    grade = forms.CharField(required=False)
    active = forms.IntegerField(initial=2, widget=forms.HiddenInput)

    def clean_score_min(self):
        question_type = self.cleaned_data['question_type']
        score_min = self.cleaned_data.get('score_min', '')
        if question_type == '1':
            if not score_min and score_min != 0:
                raise forms.ValidationError('This field is required.')
            else:
                score_max = self.cleaned_data.get('score_max', '')
                if score_min > score_max:
                    raise forms.ValidationError('Score Min Should be Less than Score Min.'
                            )
        return score_min

    def clean_score_max(self):
        question_type = self.cleaned_data['question_type']
        score_max = self.cleaned_data.get('score_max', '')
        if question_type == '1':
            if not score_max and score_max != 0:
                raise forms.ValidationError('This field is required.')
            else:
                score_min = self.cleaned_data.get('score_min', '')
                if score_min > score_max:
                    raise forms.ValidationError('Score Max Should be Grater than Score Min.'
                            )
        return score_max

    def clean_grade(self):
        question_type = self.cleaned_data['question_type']
        grade = self.cleaned_data.get('grade', '')
        if question_type == '2':
            if not grade:
                raise forms.ValidationError('This field is required.')

        return grade

    class Meta:

        model = Question



class UserAssessmentPermissions_Form(ModelForm):
    #active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:

        model = UserAssessmentPermissions
    '''   
    def __init__(self,  *args, **kwargs):
         #self.args=args
         #self.kwargs=kwargs
         super(Answer_Form, self).__init__(*args, **kwargs)
    '''
    def save(self,commit=True):
          #print self.data,'DAAAAAAAAAAAAAAAAAAAAAAAAAa'
          return CustomizeSave(self,UserAssessmentPermissions_Form)

class Assessment_StudentGroup_Association_Form(ModelForm):
    #active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:

        model = Assessment_StudentGroup_Association
    def save(self,commit=True):
          #print self.data,'DAAAAAAAAAAAAAAAAAAAAAAAAAa'
          return CustomizeSave(self,Assessment_StudentGroup_Association_Form)
class Assessment_Class_Association_Form(ModelForm):
    #active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
    
        model = Assessment_Class_Association
    def save(self,commit=True):
          #print self.data,'DAAAAAAAAAAAAAAAAAAAAAAAAAa'
          return CustomizeSave(self,Assessment_Class_Association_Form)

class Assessment_Institution_Association_Form(ModelForm):
    #active = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    class Meta:
    
        model = Assessment_Institution_Association
    def save(self,commit=True):
          #print self.data,'DAAAAAAAAAAAAAAAAAAAAAAAAAa'
          return CustomizeSave(self,Assessment_Institution_Association_Form)


class Answer_Form(ModelForm):
    #current_user = forms.IntegerField(initial=2, widget=forms.HiddenInput)
    #username = forms.CharField(initial=2, widget=forms.HiddenInput)
    #path_info = forms.IntegerField(initial='/', widget=forms.HiddenInput)
    class Meta:

        model = Answer
    '''   
    def __init__(self,  *args, **kwargs):
         #self.args=args
         #self.kwargs=kwargs
         super(Answer_Form, self).__init__(*args, **kwargs)
    '''
    def save(self,commit=True):
          #print self.data,'DAAAAAAAAAAAAAAAAAAAAAAAAAa'
          return CustomizeSave(self,Answer_Form)
    

class UserCreationFormExtended(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['groups'].required = True

    def save(self, commit=True):
        user = super(UserCreationFormExtended, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            user.groups = self.cleaned_data['groups']
            user.save()
        return user

    class Meta:

        model = User
        fields = ('username', 'password1', 'password2', 'groups')


