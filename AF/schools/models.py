from django.db import models
import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from object_permissions import register
from fullhistory import register_model
# Table Structure For Klp
register_model(User)
class Institution_Category(models.Model):
	'''This Class stores the Institution Category Information'''
	name = models.CharField(max_length = 50)
	categoryType = models.IntegerField()
	def __unicode__(self):
		return "%s"%self.name
register_model(Institution_Category)

Institution_Genders=['boys','girls','co-ed']
Institution_Gender = []
for school in Institution_Genders:
	type_school=(school,school)
	Institution_Gender.append(type_school)

Sex = ['male','female']
Gender = []
for gender in Sex:
	genders=(gender,gender)
	Gender.append(genders)

alphaList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
Alpha_list = []
for typ in alphaList:
	typs=(typ,typ)
	Alpha_list.append(typs)


goups = ["Class", "Center"]
Group_Type=[]
for gTyp in goups:
	typs = (gTyp, gTyp)
	Group_Type.append(typs)



quesType = ['Marks','Grade']
QuestionType = []
for indx,qType in enumerate(quesType):
    typs = (indx+1,qType)
    QuestionType.append(typs)


rel_type = ['Mother','Father','Siblings']
Relation_Type = []
for Rtype in rel_type:
	reltyps = (Rtype,Rtype)
	Relation_Type.append(reltyps)

class Moi_Type(models.Model):
	'''This Class stores the Mother Toungue (Languages) Information'''
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return "%s"%self.name

register_model(Moi_Type)

class Institution_Management(models.Model):
	'''This Class stores the Institution Management Information'''
	name = models.CharField(max_length = 50)

	def __unicode__(self):
		return "%s"%self.name
register_model(Institution_Management) # Register model for to store information in fullhistory
		
		
class Institution_address(models.Model):
	''' This class stores information about institution address '''
	address = models.CharField(max_length = 1000)
	area = models.CharField(max_length = 200, blank=True, null=True)
	pincode = models.CharField(max_length = 100, blank=True, null=True)
	landmark = models.CharField(max_length = 1000, blank=True, null=True, help_text="Can be comma separated")
	instidentification = models.CharField(max_length = 1000, blank=True, null=True, help_text="Can be comma separated")
	routeInformation = models.CharField(max_length = 500, blank=True, null=True, help_text="Can be comma separated")		
register_model(Institution_address)  # Register model for to store information in fullhistory


class Boundary_Category(models.Model):
	'''This Class stores the Boundary Category Information'''
	boundary_category = models.CharField(max_length = 100)

	def __unicode__(self):
		return "%s" %(self.boundary_category)
register_model(Boundary_Category)  # Register model for to store information in fullhistory

class Boundary_Type(models.Model):
	'''This Class stores the Boundary Type Information'''
	boundary_type = models.CharField(max_length = 100)

	def __unicode__(self):
		return "%s" %(self.boundary_type)
register_model(Boundary_Type)  # Register model for to store information in fullhistory

class Staff_Type(models.Model):
	'''This Class stores information about Staff Type'''
	staffType = models.CharField(max_length = 100)
	categoryType = models.IntegerField()
	
	def __unicode__(self):
		return "%s" %(self.staffType)
register_model(Staff_Type)  # Register model for to store information in fullhistory
		
class Staff_Qualifications(models.Model):
	''' This Class Stores Information about staff qualification '''
	qualification = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return '%s' %(self.qualification)			
register_model(Staff_Qualifications)  # Register model for to store information in fullhistory

class Boundary(models.Model):
	'''This class specifies the longitude and latitute of the area'''
	parent = models.ForeignKey("self",blank=True,null=True)
	name = models.CharField(max_length = 300)
	boundary_category = models.ForeignKey(Boundary_Category,blank=True,null=True)
	boundary_type = models.ForeignKey(Boundary_Type,blank=True,null=True)
	active = models.IntegerField(blank = True, null = True,default=2)

	class Meta:
		""" Used For ordering """
		ordering = ["name"]
	
	def __unicode__(self):
		return "%s"%(self.name)

	def getChild(self, boundaryType):
		if Boundary.objects.filter(parent__id=self.id ,active=2, boundary_type = boundaryType).count():
			return True
		elif Institution.objects.filter(boundary__id=self.id ,active=2).count():
			return True
		else:
			return False

	def getModuleName(self):
		return 'boundary'

	def getViewUrl(self, boundaryType):
		return '<a href="/boundary/%s/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="Boundary" /> &nbsp; <span id="boundary_%s_text">%s</span> </a>' % (self.id, boundaryType, self.name, self.id, self.name)

	def CreateNewFolder(self, boundaryType):
		return '<span><a href="/boundary/%s/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="Boundary" /> &nbsp; <span id="boundary_%s_text">%s</span> </a></span>' % (self.id, boundaryType, self.name, self.id, self.name)

	def get_view_url(self, boundaryType):
		return '/boundary/%s/%s/view/' % (self.id, boundaryType)
	
	def get_edit_url(self):
		return '/boundary/%s/update/' %(self.id)

	def get_update_url(self):
		return '/boundary/%d/update/' %(self.id)
		
	def getPermissionChild(self, boundaryType):
		if Boundary.objects.filter(parent__id=self.id ,active=2, boundary_type = boundaryType) :
			return True
		else:
			return False
	
	def getPermissionViewUrl(self):
		return '<a href="/boundary/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' % (self.id, self.name, self.name)
		
	def getAssessmentPermissionViewUrl(self, assessment_id):
		return '<a href="/boundary/%s/assessmentpermissions/%s/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' % (self.id, assessment_id , self.name, self.name)
		
	def showPermissionViewUrl(self, userSel):
		if self.boundary_category.id in [9, 10, 13, 14]:
			return '<a href="/show/%s/user/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' % (self.id, userSel, self.name, self.name) 
		else:
			return '<a href="/list/%s/user/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' % (self.id, userSel, self.name, self.name) 
		

register_model(Boundary)

class Institution(models.Model):
	''' It stores the all data regarding Institutions'''
	boundary = models.ForeignKey(Boundary)
	dise_code = models.CharField(max_length = 14,blank=True,null=True)
	name = models.CharField(max_length = 300)
	cat = models.ForeignKey(Institution_Category,blank=True,null=True)
	institution_gender = models.CharField(max_length=10,choices=Institution_Gender,default="co-ed")
	languages = models.ManyToManyField(Moi_Type)
	mgmt = models.ForeignKey(Institution_Management,default="ed")
	inst_address = models.ForeignKey(Institution_address,blank=True,null=True)
	active = models.IntegerField(blank = True, null = True,default=2)

        class Meta:
		ordering = ["name"]
	
	def __unicode__(self):
		return "%s"%(self.name)

	def get_all_cat(self, categoryType):
		return Institution_Category.objects.all(categoryType = categoryType)

	def getChild(self):
		if StudentGroup.objects.filter(institution__id = self.id,active=2).count():
			return True
		else:
			return False


	def get_all_mgmt(self):
		return institution_Management.objects.all()

	def get_all_languages(self):
		return Moi_Type.objects.all()

	def getModuleName(self):
		return 'institution'

	def get_update_url(self):
		return '/institution/%d/update/' %(self.id)

	def getViewUrl(self):
		return '<a href="/institution/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/institution.gif" title="institution" /> &nbsp; <span id="institution_%s_text">%s</span> </a>' %(self.id, self.name, self.id, self.name)

	def get_view_url(self):
		return '/institution/%s/view/' %(self.id)
		
	def get_edit_url(self):
		return '/institution/%s/update/' %(self.id)

	def CreateNewFolder(self):
		retStr = '<span><a href="/institution/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/institution.gif" title="institution" /> &nbsp; <span id="institution_%s_text">%s</span></a> </span>' %(self.id, self.name, self.id, self.name)
		groupObjects = StudentGroup.objects.filter(institution__id = self.id,active=2)
		if groupObjects:
			retStr = "<div class='hitarea hasChildren-hitarea collapsable-hitarea'></div>"+retStr+"<ul>"
			for groupObj in groupObjects:
				groupName = groupObj.name
				if groupName == '0':
					groupName = 'Anganwadi Class'
				retStr = retStr + """<li id="%s"><span><a class="KLP_treetxt" onclick="return KLP_View(this)" href="/studentgroup/%s/view/" title="%s"> <img title="Class" src="/static_media/tree-images/reicons/studentgroup_Class.gif"> <span id="studentgroup_%s_text">%s</span>  </a></span></li>""" %(groupObj.id, groupObj.id, groupName, groupObj.id, groupName)
			retStr = retStr + "</ul>"
		return retStr


register(['Acess'], Institution) # Register model for Object permissions
register_model(Institution)  # Register model for to store information in fullhistory

from django.db.models.signals import post_save, pre_save
from schools.receivers import KLP_NewInst_Permission
# Call KLP_NewInst_Permission method on Institution save
post_save.connect(KLP_NewInst_Permission, sender=Institution) 

class Child(models.Model):
	''' This class stores the personnel information of the childrens'''
	firstName = models.CharField(max_length = 50)
	middleName = models.CharField(max_length = 50,blank=True,null=True)
	lastName = models.CharField(max_length = 50,blank=True,null=True)
	uid = models.CharField(max_length = 100,blank=True,null=True)
	dob = models.DateField(max_length = 20)
	gender = models.CharField(max_length=10,choices=Gender,default="male")
	mt =  models.ForeignKey(Moi_Type,default="kannada")

	class Meta: 
		ordering = ["firstName", "middleName", "lastName"]

	def __unicode__(self):
		return "%s"%(self.firstName)

	def getRelations(self):
		return Relations.objects.filter(child__id=self.id)

	def getFather(self):
		return Relations.objects.get(relation_type="Father",child__id=self.id)

	def getMother(self):
		return Relations.objects.get(relation_type="Mother",child__id=self.id)

	def getStudent(self):
		return Student.objects.get(child__id=self.id)

	def get_view_url(self):
		return '/child/%s/view/' %(self.id)

	def get_update_url(self):
		return '/child/%d/update/' %(self.id)
register_model(Child)		# Register model for to store information in fullhistory

class Relations(models.Model):
    ''' This class stores relation information of the childrens'''
    relation_type = models.CharField(max_length=10,choices=Relation_Type,default="Mother")
    first_name = models.CharField(max_length = 100)
    middle_name = models.CharField(max_length = 50,blank=True,null=True)
    last_name = models.CharField(max_length = 50,blank=True,null=True)
    child = models.ForeignKey(Child)
    
    def __unicode__(self):
		return "%s"%(self.first_name)

    def get_view_url(self):
		return ''
register_model(Relations)  # Register model for to store information in fullhistory

class StudentGroup(models.Model):
	''' Here it holds the informaion of the class and section of the Institutions'''
	institution = models.ForeignKey(Institution)
	name = models.CharField(max_length=50)
	section = models.CharField(max_length=10,choices=Alpha_list,blank=True,null=True)
	active = models.IntegerField(blank = True, null = True,default=2)
	group_type = models.CharField(max_length=10,choices=Group_Type,default="Class")

	class Meta: 
		unique_together = (('institution', 'name', 'section'),) 
		ordering = ["name", "section"]

	def __unicode__(self):
		return "%s"%(self.name)


	def getChild(self):
		return False


	def getModuleName(self):
		return 'studentgroup'

	def get_update_url(self):
		return '/studentgroup/%d/update/' %(self.id)

	def getViewUrl(self):
		sec = self.section
	    	if sec == None:
	    		sec = ''
		groupName = self.name
		if groupName == '0':
			groupName = 'Anganwadi Class'
		return '<a href="/studentgroup/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/studentgroup_%s.gif" title="%s" /> <span id="studentgroup_%s_text">%s %s</span> </a>' %(self.id, groupName, sec, self.group_type, self.group_type, self.id, groupName, sec)
		
	def getStudentProgrammeUrl(self, filter_id, secfilter_id):
	    groupName = self.name
	    if groupName == '0':
	    	groupName = 'Anganwadi Class'
	    sec = self.section
	    if sec == None:
	    	sec = ''	
	    return '<a href="/studentgroup/%s/programme/%s/assessment/%s/view" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/studentgroup_%s.gif" title="%s" /> &nbsp; <span id="studentgroup_%s_text">%s %s</span> </a>' %(self.id, filter_id, secfilter_id, groupName, sec, self.group_type, self.group_type, self.id,  groupName, sec)

	def get_view_url(self):
		return '/studentgroup/%s/view/' %(self.id)

	def CreateNewFolder(self):
		sec = self.section
	    	if sec == None:
	    		sec = ''
		groupName = self.name
		if groupName == '0':
			groupName = 'Anganwadi Class'
		return '<span><a href="/studentgroup/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/studentgroup_%s.gif" title="%s" /> &nbsp; <span id="studentgroup_%s_text">%s %s</span> </a></span>' %(self.id, groupName, sec, self.group_type, self.group_type, self.id,  groupName, sec)
register_model(StudentGroup)  # Register model for to store information in fullhistory

class Academic_Year(models.Model):
	''' Its stores the academic years information'''
	name = models.CharField(max_length = 20, unique= True)
	
	def __unicode__(self):
		return self.name
register_model(Academic_Year)  # Register model for to store information in fullhistory

def current_academic():
    ''' To select current academic year'''
    now = datetime.date.today()
    currentYear = int(now.strftime('%Y'))
    currentMont = int(now.strftime('%m'))
    if currentMont>=1 and currentMont<=5:
        academic = '%s-%s' %(currentYear-1, currentYear)
    else:
        academic = '%s-%s' %(currentYear, currentYear+1)
    try:
        academicObj = Academic_Year.objects.get(name=academic)
        return academicObj
    except Academic_Year.DoesNotExist:
        return 1

class Staff(models.Model):
	'''This Class stores the Institution Worker(Staff) Information'''
	institution = models.ForeignKey(Institution, blank = True, null = True)
	firstName = models.CharField(max_length = 50)
	middleName = models.CharField(max_length = 50,blank=True,null=True)
	lastName = models.CharField(max_length = 50,blank=True,null=True)
	uid = models.CharField(max_length = 100,blank=True,null=True)
	doj = models.DateField(max_length = 20,blank=True,null=True)
	gender = models.CharField(max_length=10,choices=Gender, default="female")
	mt =  models.ForeignKey(Moi_Type,default="kannada")
	#qualification = models.ForeignKey(Staff_Qualifications,blank=True,null=True, default=1)
        qualification = models.ManyToManyField(Staff_Qualifications,blank=True,null=True)
	staff_type = models.ForeignKey(Staff_Type, default=1)
	active = models.IntegerField(blank = True, null = True,default=2)

	class Meta: 
		ordering = ["firstName", "middleName", "lastName"]

	def __unicode__(self):
		return "%s %s %s"%(self.firstName, self.middleName, self.lastName)
		
	def getAssigendClasses(self):
		return 	StudentGroup.objects.filter(staff_studentgrouprelation__staff__id = self.id, staff_studentgrouprelation__active=2)
register_model(Staff)  # Register model for to store information in fullhistory

class Student(models.Model):
	''' This class gives information regarding the students class , academic year and personnel details'''
	child = models.ForeignKey(Child)
	otherStudentId = models.CharField(max_length = 100,blank = True, null = True)
	active = models.IntegerField(blank = True, null = True,default=2)

	class Meta:
		ordering = ["child__firstName"]
	
	def GetName(self):
		return self.child.firstName

	def __unicode__(self):
		return "%s"%(self.child)

	def getChild(self):
		return False

	def get_all_academic_years(self):
		return Academic_Year.objects.all()

	def get_all_languages(self):
		return Moi_Type.objects.all()

	def getModuleName(self):
		return 'student'

	def get_update_url(self):
		return '/student/%d/update/' %(self.id)

	def getViewUrl(self):
		return '<a href="/student/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> %s </a>' %(self.id,self.child, self.child)

	def get_view_url(self):
		return '/student/%s/view/' %(self.id)

	def CreateNewFolder(self):
		return '<span><img src="/static_media/tree-images/reicons/student.gif" title="student" /> &nbsp;<a href="/boundary/%s/institution/%s/classes/%s/sections/%s/students/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt"> %s </a><a href="/boundary/%s/institution/%s/classes/%s/sections/%s/students/%s/edit/" onclick="return KLP_View(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'student\', \'%s\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span></span>' %(self.class_section.classname.sid.boundary.id, self.class_section.classname.sid.id, self.class_section.classname.id, self.class_section.id,self.id,self.name, self.class_section.classname.sid.boundary.id, self.class_section.classname.sid.id, self.class_section.classname.id,self. class_section.id, self.id, self.id, self.name)

register_model(Student)  # Register model for to store information in fullhistory

class Student_StudentGroupRelation(models.Model):
	'''This Class stores the Student and Student Group Realation Information'''
	student = models.ForeignKey(Student)
	student_group = models.ForeignKey(StudentGroup)	
	academic = models.ForeignKey(Academic_Year, default=current_academic)
	active = models.IntegerField(blank = True, null = True,default=2)
	
	class Meta: 
		unique_together = (('student', 'student_group', 'academic'),) 
register_model(Student_StudentGroupRelation)	# Register model for to store information in fullhistory
	
class Staff_StudentGroupRelation(models.Model): 
	'''This Class stores the Staff and Student Group Realation Information'''
 	staff = models.ForeignKey(Staff) 
 	student_group = models.ForeignKey(StudentGroup)  
 	academic = models.ForeignKey(Academic_Year, default=current_academic) 
 	active = models.IntegerField(blank = True, null = True,default=2) 	
 	
 	class Meta: 
		unique_together = (('staff', 'student_group', 'academic'),) 	
register_model(Staff_StudentGroupRelation)		# Register model for to store information in fullhistory

def default_end_date():
    ''' To select academic year end date'''
    now = datetime.date.today()
    currentYear = int(now.strftime('%Y'))
    currentMont = int(now.strftime('%m'))
    if currentMont>5:
        academic_end_date = datetime.date(currentYear+1, 5, 30)
    else:
        academic_end_date = datetime.date(currentYear, 5, 30)
    return academic_end_date


class Programme(models.Model):
	""" This class Stores information about Programme """
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 500,blank = True, null = True)
	startDate = models.DateField(max_length = 20, default=datetime.date.today)
	endDate = models.DateField(max_length = 20, default=default_end_date)
	programme_institution_category = models.ForeignKey(Boundary_Type,blank=True,null=True)
	active = models.IntegerField(blank = True, null = True,default=2)

	class Meta: 
		ordering = ["name"]

	def __unicode__(self):
		return "%s (%s-%s)"%(self.name, self.startDate.strftime("%Y"), self.endDate.strftime("%Y"))

	def get_view_url(self):
		return '/programme/%s/view/' %self.id
		
	def get_edit_url(self):
		return '/programme/%s/update/' %(self.id)

	def getChild(self):
		if Assessment.objects.filter(programme__id=self.id ,active=2).count():
			return True
		else:
			return False

	def getModuleName(self):
		return 'programme'

	def getViewUrl(self):
		return '<a href="/programme/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s (%s-%s)"> <img src="/static_media/tree-images/reicons/programme.gif" title="Programme" /> &nbsp; <span id="programme_%s_text">%s (%s-%s)</span> </a>' %(self.id, self.name, self.startDate.strftime("%Y"), self.endDate.strftime("%Y"), self.id, self.name, self.startDate.strftime("%Y"), self.endDate.strftime("%Y"))

	def CreateNewFolder(self):
		return '<span><a href="/programme/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s (%s-%s)"> <img src="/static_media/tree-images/reicons/programme.gif" title="Programme" /> &nbsp; <span id="programme_%s_text">%s (%s-%s)</span></a></span>' %(self.id,self.name, self.startDate.strftime("%Y"), self.endDate.strftime("%Y"), self.id, self.name, self.startDate.strftime("%Y"), self.endDate.strftime("%Y"))	
register_model(Programme)   # Register model for to store information in fullhistory

class Assessment(models.Model):
    """ This class stores information about Assessment """
    programme = models.ForeignKey(Programme)
    name =  models.CharField(max_length = 100)   
    startDate = models.DateField(max_length = 20, default=datetime.date.today)
    endDate = models.DateField(max_length = 20, default=default_end_date)
    query = models.CharField(max_length = 500,blank = True, null = True)
    active = models.IntegerField(blank = True, null = True,default=2)
    
    class Meta: 
		unique_together = (('programme', 'name'),)
		ordering = ["startDate"]

    def __unicode__(self):
        return "%s"%(self.name)

    def get_view_url(self):
		return '/assessment/%s/view/' %self.id 

    def get_edit_url(self):
    	return '/assessment/%s/update/' %(self.id)

    def getChild(self):
	if Question.objects.filter(assessment__id=self.id, active=2).count():
		return True
	else:
		return False

    def getViewUrl(self):
	return '<a id="assessment_%s_view" href="/assessment/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/assessment.gif" title="Assessment" /> &nbsp; <span id="assessment_%s_text">%s</span> </a>' %(self.id, self.id, self.name, self.id, self.name)

    def getModuleName(self):
		return 'assessment'

    def CreateNewFolder(self):
		return '<span><a id="assessment_%s_view" href="/assessment/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/assessment.gif" title="Assessment" /> &nbsp; <span id="assessment_%s_text">%s</span></a></span>' %(self.id, self.id, self.name, self.id, self.name)
register_model(Assessment)  # Register model for to store information in fullhistory

class Assessment_StudentGroup_Association(models.Model):
	'''This Class stores the Assessment and Student Group Association Information'''
	assessment = models.ForeignKey(Assessment)
	student_group = models.ForeignKey(StudentGroup)	
	active = models.IntegerField(blank = True, null = True,default=2)
	
	class Meta: 
		unique_together = (('assessment', 'student_group'),) 
register_model(Assessment_StudentGroup_Association)  # Register model for to store information in fullhistory

class Question(models.Model):
    """ This class stores Assessment detail information """
    assessment = models.ForeignKey(Assessment)
    name = models.CharField(max_length = 200)
    questionType = models.IntegerField(choices=QuestionType,default=1)
    scoreMin = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    scoreMax = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    grade = models.CharField(max_length = 100,blank = True, null = True)
    order = models.IntegerField()
    doubleEntry = models.BooleanField(default=True)
    active = models.IntegerField(blank = True, null = True,default=2)
    
    class Meta: 
		unique_together = (('assessment', 'name'),)
		ordering = ["order"]

    def __unicode__(self):
        return self.name

    def getAllGrades(self):
        return gradeList

    def getSelectedGrades(self):
        if self.grade:
            return  self.grade.split(',')
        else:
            return ''

    def getChild(self):
        return False

    def getViewUrl(self):
        return '<a href="/question/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/question.gif" title="Question" /> &nbsp; <span id="question_%s_text">%s</span> </a>' %(self.id, self.name, self.id, self.name)

    def getModuleName(self):
        return 'question'

    def get_view_url(self):
        return  '/question/%s/view/' %(self.id)

    def get_edit_url(self):
    	return '/question/%s/update/' %(self.id)

    def CreateNewFolder(self):
		return '<span><a href="/question/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/question.gif" title="Question" /> &nbsp; <span id="question_%s_text">%s</span></a></span>' %(self.id, self.name, self.id, self.name)

register_model(Question)  # Register model for to store information in fullhistory

class Answer(models.Model):
    """ This class stores information about student marks and grade """
    question  = models.ForeignKey(Question)
    student = models.ForeignKey(Student)
    answerScore = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null = True)
    answerGrade = models.CharField(max_length = 30, blank = True, null = True)
    doubleEntry = models.IntegerField(blank = True, null = True,default=0)
    status = models.IntegerField(blank = True, null = True,)
    user1 = models.ForeignKey(User, blank = True, null = True, related_name = 'user1')
    user2 = models.ForeignKey(User, blank = True, null = True, related_name = 'user2')
    creationDate = models.DateField(default=datetime.date.today, blank = True, null = True)
    lastModifiedDate = models.DateField(default=datetime.date.today, blank = True, null = True)
    lastmodifiedBy = models.ForeignKey(User, blank = True, null = True, related_name = 'lastmodifiedBy')
    
    class Meta: 
		unique_together = (('question', 'student'),)
register_model(Answer)   # Register model for to store information in fullhistory

class UserAssessmentPermissions(models.Model):
	""" This class stores information about user, instituion and assessment permissions"""
	user = models.ForeignKey(User)
	instituion = models.ForeignKey(Institution)
	assessment = models.ForeignKey(Assessment)
	access = models.BooleanField(default=True)
	
	class Meta: 
		unique_together = (('user', 'instituion', 'assessment'),)
