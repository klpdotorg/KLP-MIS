from django.db import models
import datetime
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

asmntttypes = ['PreTest','PostTest']
AssessmentType = []
for typ in asmntttypes:
	typs=(typ,typ)
	AssessmentType.append(typs)	



quesType = ['Marks','Grade']	
QuestionType = []	
for qType in quesType:
    typs = (qType,qType)
    QuestionType.append(typs)
	
	
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

"""Questions = ['text','numeric','radio']
Question_Type = []
for question in Questions:
	QuestionType = (question,question)
	Question_Type.append(QuestionType)
"""

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
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'boundary\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a id="%s_add" href="/boundary/creator/" style="color:#75ad0a;" onclick="return schoolAdd(this);call_js(this);">&nbsp;<img src="/static_media/images/boundary_add.gif" title="Add Boundary" /></a><a href="/boundary/%s/schools/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/school_add.gif" title="Add School"/></a><a href="/child/%s/creator/" onclick="return schoolView(this)">&nbsp;<img  title="Add Child" src="/static_media/images/child_add.gif"/></a><a href="/boundary/%s/partition/" onclick="return schoolView(this)">&nbsp;<img title="Partition" src="/static_media/images/partation.gif"/></a>' % (self.id,self.id,self.id,self.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" /> &nbsp;<a href="/boundary/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'boundary\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a id="%s_add" href="/boundary/creator/" style="color:#75ad0a;" onclick="return schoolAdd(this);call_js(this);">&nbsp;<img src="/static_media/images/boundary_add.gif" title="Add Boundary" /></a><a href="/boundary/%s/schools/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/school_add.gif" title="Add School"/></a> <a href="/child/%s/creator/" onclick="return schoolView(this)">&nbsp;<img  title="Add Child" src="/static_media/images/child_add.gif"/></a><a href="/boundary/%s/partition/" onclick="return schoolView(this)">&nbsp;<img title="Partition" src="/static_media/images/partation.gif"/></a></span>' % (self.id, self.name, self.id, self.id,self.id,self.id,self.id,self.id)

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

	def get_school_types(self):
		typeList = ['%s' %(schType[0]) for schType in School_Type]
		return typeList

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
		
	def get_view_url(self):
		return '/child/%s/view/' %(self.id)	

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
		deleteUrl = '&nbsp;<span class="delConf" onclick="deleteSchool(\'%s\', \'class\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/classes/%s/section/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/sections_add.gif" title="Add Section"/></a>' %( self.id, self.id)
		
		return  deleteUrl   

	def get_view_url(self):
		return '/boundary/%s/schools/%s/classes/%s/view/' %(self.sid.boundary.id,self.sid.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/class.gif" title="class" /> &nbsp;<a href="/boundary/%s/schools/%s/classes/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/classes/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'class\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/classes/%s/section/creator/" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/sections_add.gif" title="Add Section"/></a></span>' %(self.sid.boundary.id,self.sid.id,self.id,self.name,self.sid.boundary.id,self.sid.id,self.id,self.id,self.id)

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

	def getStudents(self):
	    return student.objects.filter(class_section__id=self.id ,active=True, academic__id=current_academic)
	    
	def getBoundarys(self):
	    boundaryObj = self.classname.sid.boundary
	    BoundaryName = boundaryObj.name
	    while(boundaryObj.parent.id !=1 ):
	        boundaryObj = boundaryObj.parent
	        BoundaryName =  '%s ---> %s' %(boundaryObj.name, BoundaryName)
	    return BoundaryName    

	def getChild(self):
		if student.objects.filter(class_section__id=self.id ,active=True) :
			return False
		else:
			return False

	def getModuleName(self):
		return 'sections'

	def getViewUrl(self):
	    sectionName = self.section
	    if sectionName == '0':
	        sectionName = 'NullSection'
	    return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id, sectionName)

	def getSection_question_student(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/question/student/" onclick="return schoolView(this)" style="color:black;">%s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id,self.section)

	def getEditUrl(self):
		return '<a href="/boundary/%s/schools/%s/classes/%s/sections/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id)

	def getDeleteUrl(self):
		return '<span class="delConf" onclick="deleteSchool(\'%s\', \'section\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/sections/%s/student/creator/" onclick="return schoolView(this)"><img src="/static_media/images/student_add.gif" title="Add Student"/></a>' %( self.id, self.id)

	def get_view_url(self):
		return '/boundary/%s/schools/%s/classes/%s/sections/%s/view/' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/sections.gif" title="sections" />&nbsp; <a href="/boundary/%s/schools/%s/classes/%s/sections/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/boundary/%s/schools/%s/classes/%s/sections/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'section\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span> <a href="/sections/%s/student/creator/" onclick="return schoolView(this)"><img src="/static_media/images/student_add.gif" title="Add Student"/></a></span>' %(self.classname.sid.boundary.id,self.classname.sid.id,self.classname.id,self.id,self.section,self.classname.sid.boundary.id, self.classname.sid.id, self.classname.id, self.id,self.id, self.id)

class Academic_Year(models.Model):
	''' Its stores the academic years information'''
	name = models.CharField(max_length = 20, unique= True)
	
	def __unicode__(self):
		return self.name
		
def current_academic():
    ''' To select current academic year'''
    now = datetime.date.today()
    currentYear = int(now.strftime('%Y'))
    currentMont = int(now.strftime('%m'))
    if currentMont>=1 and currentMont<6:
        academic = '%s-%s' %(currentYear-1, currentYear)
    else:
        academic = '%s-%s' %(currentYear, currentYear+1)
    try:    
        academicObj = Academic_Year.objects.get(name=academic)
        return academicObj.id
    except Academic_Year.DoesNotExist:
        return 1
   

class student(models.Model):
	''' This class gives information regarding the students class , academic year and personnel details'''
	class_section = models.ForeignKey(Sections)
	name = models.ForeignKey(Child) 
	academic = models.ForeignKey(Academic_Year, default=current_academic)
	active = models.BooleanField(default=True)
	
	def GetName(self):
		return self.name.firstName

	def __unicode__(self):
		return "%s---->%s---->%s"%(self.name,self.class_section,self.academic)

	def getChild(self):
		return False
	
	def getBoundary(self):
		return self.class_section.classname.sid.boundary

	def getAssessmentQuestions(self):
		boundary = self.name.boundary
		question_list=[]
		programme_list = Programme.objects.filter(boundary=boundary)
		for prg in programme_list:
			assement_list = Assessment.objects.filter(programme=prg)
			for assem in assement_list:
				question_list = Question.objects.filter(assessment=assem)
		return question_list

	def get_all_academic_years(self):
		return Academic_Year.objects.all()

	def get_all_languages(self):
		return Moi_Type.objects.all()

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



class Programme(models.Model):
	""" This class Stores information about Programme """
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 500,blank = True, null = True)
	startDate = models.DateField(max_length = 20)
	endDate = models.DateField(max_length = 20)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "%s"%(self.name)

	def get_view_url(self):
		return '/programme/%s/view/' %self.id

	def getChild(self):
		if Assessment.objects.filter(programme__id=self.id ,active=True) :
			return True
		else:
			return False

	def getModuleName(self):
		return 'programme'

	def getViewUrl(self):
		return '<a href="/programme/%s/view/" onclick="return schoolView(this)" style="color:#000;">%s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.id, self.name)

	def getEditUrl(self):
		return '<a href="/programme/%s/edit/" onclick="return schoolView(this)" style="color:#000;">&nbsp;<img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.id)

	def getDeleteUrl(self):
		return '&nbsp;<span class="delConf" onclick="deleteSchool(\'%s\', \'programme\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/assessment/%s/creator/" style="color:#000;" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/assessment_add.gif" title="Add Assessment"/></a>' %(self.id, self.id)
		
	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/programme.gif" title="Programme" /> &nbsp;<a href="/programme/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/programme/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'programme\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span></span>' %(self.id,self.name,self.id,self.id)	


class Question(models.Model):
    """ This class stores information about Quetion """
    question = models.CharField(max_length=200, blank = True, null = True)
    questionType = models.CharField(max_length = 30,choices=QuestionType,default="Marks")
    tags = models.CharField(max_length=300, blank = True, null = True)
    
    def __unicode__(self):
        return "%s"%(self.question)

    def get_view_url(self):
    	return '/question/%s/view/' %self.id

class Assessment(models.Model):
    """ This class stores information about Assessment """
    programme = models.ForeignKey(Programme)
    name =  models.CharField(max_length = 100)   
    startDate = models.DateField(max_length = 20,blank = True, null = True)
    endDate = models.DateField(max_length = 20,blank = True, null = True)
    assessmentType = models.CharField(max_length = 30,choices=AssessmentType,default="PreTest")
    query = models.CharField(max_length = 500)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s"%(self.name)
        
    def get_view_url(self):
		return '/assessment/%s/view/' %self.id    

    def getChild(self):
        if AssessmentDetail.objects.filter(assessment__id=self.id):
            return True
        else:
            return False

    def getViewUrl(self):
	return '<a href="/assessment/%s/view/" onclick="return schoolView(this)" style="color:#000;">%s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.id, self.name)

    def getEditUrl(self):
        return '<a href="/assessment/%s/edit/" onclick="return schoolView(this)" style="color:#000;">&nbsp;<img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.id)

    def getDeleteUrl(self):
	return '&nbsp;<span class="delConf" onclick="deleteSchool(\'%s\', \'assessment\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/assessmentdetail/%s/creator/" style="color:#000;" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/add_icon.gif" title="Add AssessmentDetail"/></a><a href="/programme/%s/assessment/%s/copy/" style="color:#000;" onclick="return schoolView(this)">&nbsp;<img width="16" src="/static_media/images/icon_copy.gif" title="Copy Questions"/></a>&nbsp;<a href="/assessment/%s/start/" onclick="return schoolView(this)"><img width="13" src="/static_media/images/start.gif" title="Start Assessment"/></a>' %(self.id, self.id, self.programme.id, self.id, self.id)

    def getModuleName(self):
		return 'assessment'
    
    def getAllAssessmentTypes(self):
        typeList = ['%s' %(assessType[0]) for assessType in AssessmentType]
        return typeList
        
    def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/assessment.gif" title="Assessment" /> &nbsp;<a href="/assessment/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/assessment/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'assessment\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span><a href="/assessmentdetail/%s/creator/" style="color:#000;" onclick="return schoolView(this)">&nbsp;<img src="/static_media/images/add_icon.gif" title="Add AssessmentDetail"/></a> <a href="/programme/%s/assessment/%s/copy/" style="color:#000;" onclick="return schoolView(this)">&nbsp;<img width="16" src="/static_media/images/icon_copy.gif" title="Copy Questions"/></a>&nbsp;<a href="/assessment/%s/start/" onclick="return schoolView(this)"><img width="13" src="/static_media/images/start.gif" title="Start Assessment"/></a></span>' %(self.id,self.name,self.id,self.id,self.id, self.programme.id, self.id, self.id)
		
		
class AssessmentDetail(models.Model):
    """ This class stores Assessment detail information """    
    assessment = models.ForeignKey(Assessment)
    #name = models.CharField(max_length = 100)
    question = models.ForeignKey(Question)   
    scoreMin = models.IntegerField()
    scoreMax = models.IntegerField()
    doubleEntry = models.BooleanField(default=True)
    required = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    def getChild(self):
        return False
    
    def getViewUrl(self):
        return '<a href="/assessmentdetail/%s/view/" onclick="return schoolView(this)" style="color:#000;">%s <img src="/static_media/images/libraryfolder.gif" title="View"/></a>' %(self.id, self.question)
        
    def getEditUrl(self):
        return '<a href="/assessmentdetail/%s/edit/" onclick="return schoolView(this)" style="color:#000;">&nbsp;<img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a>' %(self.id)
        
    def getDeleteUrl(self):
        return '&nbsp;<span class="delConf" onclick="deleteSchool(\'%s\', \'assessmentdetail\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span>' %(self.id)
        
    def getModuleName(self):
        return 'assessmentdetail'
        
    def get_view_url(self):
        return  '/assessmentdetail/%s/view/' %(self.id)
        
    def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/assessmentdetail.gif" title="assessmentdetail" /> &nbsp;<a href="/assessmentdetail/%s/view/" onclick="return schoolView(this)" style="color:black;"> %s<img src="/static_media/images/libraryfolder.gif" title="View"/></a><a href="/assessmentdetail/%s/edit/" onclick="return schoolView(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'assessmentdetail\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span></span>' %(self.id,self.question,self.id,self.id)    
    

class Answer(models.Model):
    """ This class stores information about student marks and grade """    
    assessment = models.ForeignKey(Assessment)
    assessmentDetail  = models.ForeignKey(AssessmentDetail)    
    student = models.ForeignKey(student)
    answer = models.CharField(max_length = 30)
    doubleEntry = models.CharField(max_length = 30,blank = True, null = True)
    
    
    
