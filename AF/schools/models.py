from django.db import models
    # Table Structure For Klp


'''Boundary_Type = (
	('Distict','Distict'),
	('Cluster','Cluster'),
	('Taluk','Taluk'),
)'''

'''School_CategoryList=['lps','lps and hps','lps, hps and hs','hps','hps and hs','hs','hs and puc','special','chs','chps and chs']
School_Category=[]
for k in School_CategoryList:
    t=(k,k)
    School_Category.append(t)'''

class School_Category(models.Model):
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return "%s"%self.name


School_Types=['boys','girls','co-ed']
School_Type = []
for school in School_Types:
	type_school=(school,school)
	School_Type.append(type_school)


Sex = ['male','female']
Gender = []
for gender in Sex:
	genders=(gender,gender)
	Gender.append(genders)

'''Languages = ['kannada','urdu','tamil','telugu','english','marathi','malayalam','hindi','konkani','sanskrit','sindhi','other','gujarathi','not known','multi lng','nepali', 'oriya','bengali']
Moi_Type = []
for language in Languages:
	Moitypes =(language,language)
	Moi_Type.append(Moitypes)'''

class Moi_Type(models.Model):
	name = models.CharField(max_length = 50)

	def __unicode__(self):
	    return "%s"%self.name 

'''Managements = ['ed','swd','local','p-a','p-ua','others','approved','ssa','kgbv','p-a-sc','p-a-st','jawahar','central','sainik','central govt','nri','madrasa-a','madrasa-ua', 'arabic-a','arabic-ua','sanskrit-a','sanskrit-ua','p-ua-sc','p-ua-st']
School_Management = []
for management in Managements:
	SchoolManagement = (management,management)
	School_Management.append(SchoolManagement)'''

class School_Management(models.Model):
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return "%s"%self.name

Questions = ['text','numeric','radio']
Question_Type = []
for question in Questions:
	QuestionType = (question,question)
	Question_Type.append(QuestionType)

class Boundary_Type(models.Model):
	'''This Class stores the Boundary Type'''
	boundary_type = models.CharField(max_length = 100)

	def __unicode__(self):
		return "%s"%self.boundary_type

class Boundary(models.Model):
	'''This class specifies the longitude and latitute of the area'''
	parent = models.ForeignKey("self",blank=True,null=True)
	name = models.CharField(max_length = 300)
	boundary_type = models.ForeignKey(Boundary_Type,blank=True,null=True)
	geo_code = models.CharField(max_length = 300)
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return "%s"%(self.name)
	
	def getChild(self):
		if Boundary.objects.filter(parent__id=self.id ,active=True) :
			return True
		elif School.objects.filter(boundary__id=self.id ,active=True):
			return True
		else:
			return False

	def getChildObjects(self):
		results=Boundary.objects.filter(parent__id=self.id,active=True)
		if not results:
			results=School.objects.filter(boundary__id=self.id,active=True)
		return results

	def getModuleName(self):
		return 'boundary'

	def get_update_url(self):
		return '/boundary/%d/update/' %(self.id)

	def getViewUrl(self):
		return '<a href="/boundary/%s/view/" onclick="return schoolView(this)" style="color:black;">%s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' % (self.id,self.name)

	def getEditUrl(self):
		return '<a href="/boundary/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' % self.id

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'boundary\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a id="%s_add" href="/boundary/creator/" style="color:#75ad0a;" onclick="return schoolAdd(this);call_js(this);">&nbsp;<img src="/static_media/images/boundary_add.gif" title="Add Boundary" /></a><a href="/boundary/%s/schools/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/school_add.gif" title="Add School"/></a><a href="/child/%s/creator/" onclick="return schoolView(this)">&nbsp;<img  title="Add Child" src="/static_media/images/child_add.gif"/></a><a href="/boundary/%s/partition/" onclick="return schoolView(this)">&nbsp;<img width="13" title="Partition" src="/static_media/images/partation.gif"/></a>' % (self.id,self.id,self.id,self.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" /> &nbsp;<a href="/boundary/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'boundary\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a id="%s_add" href="/boundary/creator/" style="color:#75ad0a;" onclick="return schoolAdd(this);call_js(this);">&nbsp;<img src="/static_media/images/boundary_add.gif" title="Add Boundary"/>&nbsp;</a><a href="/boundary/%s/schools/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/school_add.gif" title="Add School"/></a> <a href="/child/%s/creator/" onclick="return schoolView(this)">&nbsp;<img title="Add Child" src="/static_media/images/child_add.gif"/></a><a href="/boundary/%s/partition/" onclick="return schoolView(this)">&nbsp;<img width="13" title="Partition" src="/static_media/images/partation.gif"/></a></span>' % (self.id, self.name, self.id, self.id,self.id,self.id,self.id,self.id)

	def get_view_url(self):
		return '/boundary/%s/view/' % self.id

"""class Address(models.Model):
	'''This class stores the address of all the schools'''
	address = models.CharField(max_length = 1000)
	landmark = models.CharField(max_length = 1000,blank=True,null=True)
	pin = models.CharField(max_length = 1000,blank=True,null=True)
	
	def __unicode__(self):
		return "%s"%(self.address)'''"""

	

class School(models.Model):
	''' It stores the all data regarding schools'''
	boundary = models.ForeignKey(Boundary)
	dise_code = models.CharField(max_length = 14,blank=True,null=True)
	name = models.CharField(max_length = 300)
	cat = models.ForeignKey(School_Category,blank=True,null=True)
	school_type = models.CharField(max_length=10,choices=School_Type,default="co-ed")
	languages = models.ManyToManyField(Moi_Type,default="kannada")
	mgmt = models.ForeignKey(School_Management,default="ed")
	address = models.CharField(max_length = 1000)
	landmark = models.CharField(max_length = 1000,blank=True,null=True)
	pincode = models.CharField(max_length = 1000,blank=True,null=True)
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return "%s"%(self.name)

	def get_all_cat(self):
		return School_Category.objects.all()

	def getChild(self):
		if Class.objects.filter(sid__id=self.id,active=True) :
			return True
		else:
			return False

	def getChildObjects(self):
		return Class.objects.filter(sid__id=self.id ,active=True)

	def get_all_mgmt(self):
		return School_Management.objects.all()

	def get_all_languages(self):
		return Moi_Type.objects.all()

	def getModuleName(self):
		return 'school'

	def get_update_url(self):
		return '/boundary/%d/schools/%d/update/' %(self.boundary.id, self.id)

	def getViewUrl(self):
		return '<a href="/boundary/%s/schools/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.boundary.id,self.id,self.name)

	def getEditUrl(self):
		return '<a href="/boundary/%s/schools/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' % (self.boundary.id,self.id)

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'school\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/schools/%s/class/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/classes_add.gif" title="Add Class"/></a>' % (self.id, self.id)

	def get_view_url(self):
		return '/boundary/%s/schools/%s/view/' %(self.boundary.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/school.gif" title="school" /> &nbsp;<a href="/boundary/%s/schools/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'school\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/schools/%s/class/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/classes_add.gif" title="Add Class"/></a> </span>' %(self.boundary.id,self.id,self.name,self.boundary.id,self.id,self.id,self.id)


class StudentManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)


class Child(models.Model):
	''' This class stores the personnel information of the childrens'''
	boundary = models.ForeignKey(Boundary)
	firstName = models.CharField(max_length = 100)
	lastName = models.CharField(max_length = 100)
	dob = models.DateField(max_length = 20,blank=True,null=True)
	gender = models.CharField(max_length=10,choices=Gender,default="male")
	mt =  models.ForeignKey(Moi_Type,default="kannada")
	mother = models.CharField(max_length = 100,blank=True,null=True)
	father = models.CharField(max_length = 100,blank=True,null=True)

	def __unicode__(self):
		return "%s"%(self.firstName)

class Class(models.Model):
	''' Here it holds the informaion of the class and section of the schools'''
	sid = models.ForeignKey(School)
	name = models.IntegerField()
	active = models.BooleanField(default=True)
	
	def __unicode__(self):
		return "%s"%(self.name)

	def getChildObjects(self):
		return Sections.objects.filter(classname__id=self.id ,active=True)

	def getChild(self):
		if Sections.objects.filter(classname__id=self.id ,active=True) :
			return True
		else:
			return False

	def getModuleName(self):
		return 'class'

	def get_update_url(self):
		return '/boundary/%d/schools/%d/classes/%d/update/' %(self.sid.boundary.id, self.sid.id, self.id)

	def getViewUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.sid.boundary.id,self.sid.id,self.id,self.name)

	def getEditUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.sid.boundary.id,self.sid.id,self.id)

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'class\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/classes/%s/section/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/sections_add.gif" title="Add Section"/></a>' %( self.id, self.id)

	def get_view_url(self):
		return '/boundary/%s/schools/%s/classes/%s/view/' %(self.sid.boundary.id,self.sid.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/class.gif" title="class" /> &nbsp;<a href="/boundary/%s/schools/%s/classes/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/classes/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'class\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/classes/%s/section/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/sections_add.gif" title="Add Section"/></a></span>' %(self.sid.boundary.id,self.sid.id,self.name,self.id,self.sid.boundary.id,self.sid.id,self.id,self.id,self.id)

SectionChoices = (
	('A','A'),
	('B','B'),
	('C','C'),
	('D','D'),
	('E','E'),
)

class Sections(models.Model):
	'''This Sections stores the Section types'''
	classname = models.ForeignKey(Class)
	section = models.CharField(max_length = 1,choices = SectionChoices)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "%s"%self.section

	def getChild(self):
		if student.objects.filter(class_section__id=self.id ,active=True) :
			return False
		else:
			return False

	def getModuleName(self):
		return 'sections'

	def getViewUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id,self.section)

	def getEditUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id)

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'section\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/sections/%s/student/creator/" onclick="return schoolView(this)"><img src="/static_media/images/student_add.gif" title="Add Student"/></a>' %( self.id, self.id)

	def get_view_url(self):
		return '/boundary/%s/schools/%s/classes/%s/sections/%s/view/' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/sections.gif" title="sections" />&nbsp; <a href="/boundary/%s/schools/%s/classes/%s/sections/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/classes/%s/sections/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'section\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span> <a href="/sections/%s/student/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/student_add.gif" title="Add Student"/></a></span>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id,self.section,self.classname.sid.boundary.id, self.classname.sid.id, self.classname.id, self.id,self.id, self.id)

class Academic_Year(models.Model):
	''' Its stores the academic years information'''
	name = models.CharField(max_length = 20)
	
	def __unicode__(self):
		return self.name

class student(models.Model):
	''' This class gives information regarding the students class , academic year and personnel details'''
	class_section = models.ForeignKey(Sections)
	name = models.ForeignKey(Child) 
	academic = models.ForeignKey(Academic_Year)
	active = models.BooleanField(default=True)
	
	def GetName(self):
		return self.name.name

	def __unicode__(self):
		return "%s---->%s---->%s"%(self.name,self.class_section,self.academic)

	def getChild(self):
		return False

	def get_all_academic_years(self):
		return Academic_Year.objects.all()

	def getModuleName(self):
		return 'student'

	def get_update_url(self):
		return '/boundary/%d/schools/%d/classes/%d/sections/%d/students/%d/update/' %(self.class_section.classname.sid.boundary.id, self.class_section.classname.sid.id, self.class_section.classname.id, self.class_section.id, self.id)

	def getViewUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.class_section.classname.sid.boundary.id,self.class_section.classname.sid.id,self.class_section.classname.id,self.class_section.id,self.id,self.name)

	def getEditUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.class_section.classname.sid.boundary.id,self.class_section.classname.sid.id,self.class_section.classname.id,self.class_section.id,self.id)

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'student\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span>' % self.id

	def get_view_url(self):
		return '/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/view/' %(self.class_section.classname.sid.boundary.id,self.class_section.classname.sid.id,self.class_section.classname.id,self.class_section.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/student.gif" title="student" /> &nbsp;<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'student\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span></span>' %(self.class_section.classname.sid.boundary.id,self.class_section.classname.sid.id,self.class_section.classname.id,self.class_section.id,self.id,self.name,self.class_section.classname.sid.boundary.id,self.class_section.classname.sid.id,self.class_section.classname.id,self.class_section.id,self.id,self.id)
