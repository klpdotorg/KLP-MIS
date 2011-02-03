# Create your views here.
from django.db import models
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.context_processors import csrf

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Template, Context, RequestContext

from models import *
from forms import *


def home1(request):
	return render_to_response("home1.html")

def home(request):
    boundaryList = Boundary.objects.filter(active=1)
    return render_to_response("home.html",{'legend':'Karnataka Learning Program ', 'title':'Karnataka Learning Program ', 'entry':'Add', 'boundaryList': boundaryList,})

def search(request):
    search_key = request.GET.get('search')
    database = request.GET.get('category')

    if search_key and database:
	if database=="school":
		Query = School.objects.filter(name__icontains=search_key)
	elif database == "child":
		Query = Child.objects.filter(name__icontains=search_key)
	elif database == "student":
		Query = Student.objects.filter(name__icontains=search_key)
	return render_to_response("search.html",{'information':Query,'category':database})
    return render_to_response("search.html")

def category_entry(request):
    if request.method == 'POST':
	form = Category_Form(request.POST)
	if form.is_valid():
		form.save()
		return render_to_response('successful.html')
	else:
		return render_to_response('category.html', {'form': form},context_instance=RequestContext(request))
    else:
	form = Category_Form()
	return render_to_response('category.html', {'form': form},context_instance=RequestContext(request))

def language_entry(request):
    if request.method == 'POST':
	form = Language_Form(request.POST)
	if form.is_valid():
		form.save()
		return render_to_response('successful.html')
	else:
		return render_to_response('languages.html', {'form': form},context_instance=RequestContext(request))
    else:
	form = Language_Form()
	return render_to_response('languages.html', {'form': form},context_instance=RequestContext(request))

def management_entry(request):
    if request.method == 'POST':
	form = Management_Form(request.POST)
	if form.is_valid():
		form.save()
		return render_to_response('successful.html')
	else:
		return render_to_response('management.html', {'form': form},context_instance=RequestContext(request))
    else:
	form = Management_Form()
	return render_to_response('management.html', {'form': form},context_instance=RequestContext(request))

def section_entry(request, class_id):
    
    if request.method == 'POST':
	form = Section_Form(request.POST)
	if form.is_valid():
		form.save()
		return render_to_response('successful.html')
	else:
		return render_to_response('section.html', {'form': form, 'class_id':class_id},context_instance=RequestContext(request))
    else:
	form = Section_Form()
	return render_to_response('section.html', {'form': form,'class_id':class_id},context_instance=RequestContext(request))
	
def treeDict(boundaryObj):
    schoolDict={}
    schoolsList = School.objects.filter(boundary=boundaryObj,active=1)
    for school in schoolsList:
	    classList = Class.objects.filter(sid=school.id,active=1)
	    classesList = []
	    for clas in classList:
	        clasDict={}
	        sectionList = []
	        sections = Sections.objects.filter(classname=clas, active=1)	    
	        for sec in sections:
	            sectionDict = {}
	            students = student.objects.filter(class_section=sec, active=1)
	            studentsList = []
	            for stud in students:
	                studentsList.append(stud)
	            sectionDict[sec] = studentsList
	            sectionList.append(sectionDict)
	        clasDict[clas] = sectionList
	        classesList.append(clasDict)
	    schoolDict[school] = classesList
    return schoolDict   
    
def treeStructure(request,boundary_id):    
    boundaryObj = Boundary.objects.get(pk=boundary_id)
    root = request.REQUEST.get('root')
    if root=='source':
        treeStuct = []
        schoolsList = School.objects.filter(boundary=boundaryObj,active=1)        
        boundaryName = '''%s<a href="/boundary/%s/edit/" onclick="return schoolEdit(this)"> <img src="/static_media/images/pagebuilder_edit.gif" width="13" title="Edit"/> </a><a href="/boundary/%s/view/" onclick="return schoolView(this)"> <img src="/static_media/images/libraryfolder.gif" width="13" title="View" name="iiiii"/> </a>''' %(boundaryObj.name, boundary_id, boundary_id)
        boudaryDict = {'text':boundaryName, 'expanded':True, 'id':'boundary_'+str(boundaryObj.id), 'classes':'folder gallery clearfix'}
        for school in schoolsList:
            schoolDict={}
            schoolName = str(school.name)
            schoolId = str(school.id)
            schoolStr = '''%s<a href="/boundary/%s/schools/%s/edit/" onclick="return schoolEdit(this)"> <img src="/static_media/images/pagebuilder_edit.gif" width="13" title="Edit"/> </a><span onclick="deleteSchool('%s', 'school')" class="delConf"><img src="/static_media/images/PageRow_delete.gif" width="11" title="Delete"/></span><a href="/boundary/%s/schools/%s/view/" onclick="return schoolView(this)"> <img src="/static_media/images/libraryfolder.gif" width="13" title="View" name="iiiii"/> </a>''' %(schoolName, boundary_id, schoolId, schoolId, boundary_id, schoolId)
            schoolDict["text"] = schoolStr
            schoolDict['classes'] = 'folder gallery clearfix' 
            schoolDict['id'] = 'school_'+schoolId
            classList = Class.objects.filter(sid=school,active=1)
            if len(classList) > 0:
                #schoolDict['expanded']=True;
                schoolDict['hasChildren']=True;                
            treeStuct.append(schoolDict) 
        boudaryDict ['children'] = treeStuct      
        finalTree = [boudaryDict]
    else:
        finalTree = []
        splRoot = root.split('_')
        if splRoot[0] == 'school':
            classList = Class.objects.filter(sid=splRoot[1],active=1)
            for clas in classList:
                classDict={}
                className = str(clas.name)
                classId = str(clas.id)
                clsStr = '''%s <a href="/akshara/class/%s/edit/?iframe3=true&amp;width=700&amp;height=200" rel="prettyPhoto[iframe3]"> <img src="/static_media/images/pagebuilder_edit.gif" width="13" title="Edit"/> </a> <span onclick="deleteSchool('%s', 'class')" class="delConf"><img src="/static_media/images/PageRow_delete.gif" width="11" title="Delete"/></span><a href="/boundary/%s/schools/%s/classes/%s/" onclick="return schoolView(this)"> <img src="/static_media/images/libraryfolder.gif" width="13" title="View" /> </a>''' %(className, classId, classId, boundary_id, splRoot[1],classId)
                classDict["text"] = clsStr
                classDict['classes'] = 'folder gallery clearfix' 
                classDict['id'] = 'class_'+classId
                secList = Sections.objects.filter(classname=clas, active=1)
                if len(classList) > 0:	   
                   classDict['hasChildren']=True;
                finalTree.append(classDict)
        elif splRoot[0] == 'class':
            sections = Sections.objects.filter(classname=splRoot[1], active=1)
            for sec in sections:
                secDict={}
                secName = str(sec.section)
                secId = str(sec.id)
                secStr = '''%s <span onclick="deleteSchool('%s', 'section')" class="delConf"><img src="/static_media/images/PageRow_delete.gif" width="11" title="Delete"/></span><a href="/boundary/%s/schools/%s/classes/%s/sections/%s" onclick="return schoolView(this)"> <img src="/static_media/images/libraryfolder.gif" width="13" title="View"/> </a>''' %(secName, secId, boundary_id,str(sec.classname.sid.id), str(sec.classname.id), secId)
                secDict["text"] = secStr
                secDict['classes'] = 'folder gallery clearfix' 
                secDict['id'] = 'section_'+secId
                students = student.objects.filter(class_section=sec, active=1)
                if len(students) > 0:	   
                   secDict['hasChildren']=True;
                finalTree.append(secDict)
        else:
            students = student.objects.filter(class_section=splRoot[1], active=1) 
            for stud in students:
                studDict={}
                studName = str(stud.child)
                studId = str(stud.id)
                studStr = '''%s <a href="/akshara/student/%s/edit/?iframe2=true&amp;width=700&amp;height=500" rel="prettyPhoto[iframe2]"> <img src="/static_media/images/pagebuilder_edit.gif" width="13" title="Edit"/> <span onclick="deleteSchool('%s', 'student')" class="delConf"><img src="/static_media/images/PageRow_delete.gif" width="11" title="Delete"/></span> <a href="/boundary/%s/schools/%s/classes/%s/sections/%s/students/%s/" onclick="return schoolView(this)"><img src="/static_media/images/libraryfolder.gif" width="13" title="View"/></a>''' %(studName, studId, studId, boundary_id, str(stud.class_section.classname.sid.id), str(stud.class_section.classname.id), str(splRoot[1]), studId)
                studDict["text"] = studStr
                studDict['classes'] = 'file gallery clearfix' 
                studDict['id'] = 'student_'+studId                
                finalTree.append(studDict)    
    return HttpResponse(simplejson.dumps(finalTree), content_type='application/json; charset=utf-8')
	
	
def section_view(request, section_id):    
    sectionObj = Sections.objects.get(pk=section_id)
    classObj = sectionObj.classname   
    schoolObj = classObj.sid
    boundaryObj = schoolObj.boundary
    boundaryName = boundaryObj.name
    schoolDict = treeDict(boundaryObj)  
    sectionName = sectionObj.section          
    return  render_to_response('section_view.html',{'legend':sectionName, 'schoolDict':schoolDict, 'title':'Section '+sectionName, 'entry':'Add', 'boundaryObj':boundaryObj, 'boundary_id':boundaryObj.id, 'classObj':classObj, 'sectionObj':sectionObj, 'schoolObj':schoolObj}) 
    
def section_delete(request):
    section_id= request.REQUEST.get('schoolId')   	
    sectionObj = Sections.objects.get(id=section_id)    
    sectionObj.active=0
    sectionObj.save()
    return HttpResponse('success') 
    
def section_entry(request,class_id):
    secObj = Sections.objects.filter(classname__id = class_id)    
    url = '/akshara/section/'+str(class_id)+'/entry/'
    sectionnames = ['%s' %(section[1]) for section in SectionChoices]
    sections = []
    for sec in secObj:
        sections.append(sec.section)
    if request.method == 'POST':
        form = Section_Form(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('successful.html')
        else:
            return render_to_response('section.html', {'form': form,'legend':'Add Sections','pagetitle':'Section Form','entry':"Add",'class_id':class_id,'secObj':secObj,'sections':sections,'sectionnames':sectionnames, 'url':url},context_instance=RequestContext(request))
    else:
        form = Section_Form()
        return render_to_response('section.html', {'form': form,'legend':'Add Sections','pagetitle':'Section Form','entry':"Add",'class_id':class_id,'secObj':secObj,'sections':sections,'sectionnames':sectionnames, 'url':url},context_instance=RequestContext(request))       
        	

def bound_type(request):
    print request.POST
    print '---------------------------'
    if request.method == 'POST':
        form = Boundary_Type_Form(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('successful.html')
        else:
            return render_to_response('boundary_type.html', {'form': form},context_instance=RequestContext(request))     	
    else:
        form = Boundary_Type_Form()        
        return render_to_response('boundary_type.html', {'form': form},context_instance=RequestContext(request))

def boundary_entry(request):
    url = '/akshara/boundary-entry/'    
    if request.method == 'POST':
        print request
        form =Boundary_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/akshara/home/')
        else:
            form = Boundary_Form(request.POST, request.FILES)
            return render_to_response('boundary_admin.html', {'form': form,'legend':'Add Boundary','pagetitle':'Boundary Form','entry':"Add","url":url,},context_instance=RequestContext(request))
    else:
        form = Boundary_Form()
        return render_to_response('boundary_admin.html', {'form': form,'legend':'Add Boundary','pagetitle':'Boundary Form','entry':"Add","url":url, },context_instance=RequestContext(request))

def boundary_edit(request, boundary_id):
    boundaryobj = Boundary.objects.get(pk=boundary_id)
    url = '/akshara/boundary/'+str(boundary_id)+'/edit/'        
    if request.method == 'POST':
        form =Boundary_Form(request.POST, request.FILES,instance=boundaryobj)
        print request.POST
        if form.is_valid():
            form.save()
            return render_to_response('successful.html')
    else:
        form = Boundary_Form(instance=boundaryobj)
        return render_to_response('boundary_admin.html', {'form': form, 'boundaryobj':boundaryobj, 'selBoundary':boundary_id, 'legend':'Edit Boundary', 'title':'Edit Boundary','url':url},context_instance=RequestContext(request))

def boundary_list(request):
    selView = request.REQUEST.get('selView')
    boundaryList = Boundary.objects.filter(active=1)
    if selView == 'partition':
        return  render_to_response('boundary_list_partition.html', {'boundaryList': boundaryList, 'legend':'Select Boundary', 'title':'Select Boundary', 'entry':'Add'})
    elif selView == 'merge':
        return  render_to_response('boundary_list_merge.html', {'boundaryList': boundaryList, 'legend':'Select Boundary', 'title':'Select Boundary', 'entry':'Add'})       
    else:
        return  render_to_response('boundary_list.html', {'boundaryList': boundaryList, 'legend':'Select Boundary', 'title':'Select Boundary', 'entry':'Add'})

def boundary_view(request, boundary_id):
    boundaryObj = Boundary.objects.get(pk=boundary_id)
    boundaryName = boundaryObj.name    
    schoolDict= treeDict(boundaryObj)    
    return  render_to_response('boundary_view.html',{'legend':boundaryName, 'schoolDict':schoolDict, 'title':boundaryName, 'entry':'Add', 'boundaryObj':boundaryObj, 'boundary_id':boundary_id})

def boundary_delete(request):
    boundary_id= request.REQUEST.get('schoolId')   	
    boundaryobj = Boundary.objects.get(pk=boundary_id)
    boundaryobj.active=0
    boundaryobj.save()
    return HttpResponse('success') 
    
def boundary_schools(request):
    boundary_id= request.REQUEST.get('selBoundary')
    boundaryObj = Boundary.objects.get(pk=boundary_id)
    boundaryName = boundaryObj.name
    schoolsList = School.objects.filter(boundary=boundaryObj,active=1)    
    return render_to_response('boundary_schools.html',{'legend':boundaryName,'title':boundaryName, 'entry':'Add','schoolsList':schoolsList,'selBoundary':boundary_id},context_instance=RequestContext(request))

def boundary_partition(request):
    print request.method
    selectedSchools = request.POST.getlist('schools')
    selBound_id = request.REQUEST.get('selBoundary')
    boundaryObj = Boundary.objects.get(pk=selBound_id)        
    boundaryNew = Boundary(parent=boundaryObj.parent, name=request.POST.get('newBoundary1'), boundary_type=boundaryObj.boundary_type, geo_code=boundaryObj.geo_code,active=1)
    boundaryNew.save()
    for school in selectedSchools:
        schoolObj = School.objects.get(pk=str(school))
        schoolObj.boundary = boundaryNew
        schoolObj.save()
    secBoundary = request.POST.get('newBoundary2')    
    try:
        boundarySec = Boundary.objects.get(name=secBoundary)
    except Boundary.DoesNotExist:
        boundarySec = Boundary(parent=boundaryObj.parent, name=secBoundary, boundary_type=boundaryObj.boundary_type, geo_code=boundaryObj.geo_code,active=1)
        boundarySec.save()
        schoolsList = School.objects.filter(boundary=boundaryObj,active=1) 
        for school in schoolsList:
            school.boundary =  boundarySec
            school.save()
        boundaryObj.active=0
        boundaryObj.save()              
    return HttpResponseRedirect('/akshara/boundary-list/')

def address_entry(request):
    if request.method == 'POST':
	form =Address_Form(request.POST, request.FILES)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    	else:
    	    form = Address_Form(request.POST, request.FILES)
    	return render_to_response('address_admin.html', {'form': form,'legend':'Add Address','pagetitle':'Address Form','entry':"Add"},context_instance=RequestContext(request))
    else:
    	    form = Address_Form()
    return render_to_response('address_admin.html', {'form': form,'legend':'Add Address','pagetitle':'Address Form','entry':"Add"},context_instance=RequestContext(request))

def address_edit(request,address_id):
    addressobj = Address.objects.get(pk=address_id)
    if request.method == 'POST':
	form =Address_Form(request.POST, request.FILES,instance=addressobj)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    else:
    	form = Address_Form(instance=addressobj)
    return render_to_response('address_admin.html', {'form': form,'legend':'Add Address','pagetitle':'Address Form','entry':"Add"},context_instance=RequestContext(request))

def school_view(request, school_id):    
    schoolObj = School.objects.get(pk=school_id)
    boundaryObj = schoolObj.boundary
    boundaryName = boundaryObj.name
    schoolDict=treeDict(boundaryObj)
    schoolName = schoolObj.name
    return  render_to_response('school_view.html',{'legend':schoolName, 'schoolDict':schoolDict, 'title':schoolName+' School', 'entry':'Add', 'boundaryObj':boundaryObj, 'boundary_id':boundaryObj.id, 'schoolObj':schoolObj})

def school_entry(request,boundary_id):        
    url = '/akshara/school/'+str(boundary_id)+'/entry/'
    if request.method == 'POST':
	form =School_Form(request.POST, request.FILES)		
	if form.is_valid():
		form.save()		
		return render_to_response('successful.html')
	else:
		form = School_Form(request.POST, request.FILES)		
	return render_to_response('school_admin.html', {'form': form,'legend':'Add School','pagetitle':'School Form','entry':"Add", 'boundary_id':boundary_id, 'url':url},context_instance=RequestContext(request))
    else:
	form = School_Form()
    return render_to_response('school_admin.html', {'form': form,'legend':'Add School','pagetitle':'School Form','entry':"Add", 'boundary_id':boundary_id, 'url':url}, context_instance=RequestContext(request))

def school_edit(request,school_id):    
    schoolobj = School.objects.get(pk=school_id)    
    boundary_id= schoolobj.boundary.id
    url = '/akshara/school/'+str(school_id)+'/edit/'    
    if request.method == 'POST':
	form =School_Form(request.POST, request.FILES,instance=schoolobj)	
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    else:
    	    form = School_Form(instance=schoolobj)
    return render_to_response('school_admin.html', {'form': form,'schoolobj':schoolobj, 'boundary_id':boundary_id, 'url':url},context_instance=RequestContext(request))
    
def school_delete(request):
    school_id= request.REQUEST.get('schoolId')   	
    schoolobj = School.objects.get(pk=school_id)    
    schoolobj.active=0
    schoolobj.save()
    return HttpResponse('success')     

def child_entry(request):

    if request.method == 'POST':
        form =Child_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redUrl = request.POST.get('redUrl')
            print redUrl
            if redUrl == 'homePage':
                return HttpResponseRedirect('/akshara/home/')
            else:
                return render_to_response('successful.html')
        else:
            form = Child_Form(request.POST, request.FILES)
            return render_to_response('child_admin.html', {'form': form,'entry':'Add','legend':'Add Child','pagetitle':'Child Form'},context_instance=RequestContext(request))
    else:
        form = Child_Form()
        redUrl = request.REQUEST.get('redUrl')
        return render_to_response('child_admin.html', {'form': form,'entry':'Add','legend':'Add Child','pagetitle':'Child Form','redUrl':redUrl},context_instance=RequestContext(request))

def child_edit(request,child_id):
    childobj = Child.objects.get(pk=child_id)
    if request.method == 'POST':
	form =Child_Form(request.POST, request.FILES,instance=childobj)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    else:
    	    form = Child_Form(instance=childobj)
    return render_to_response('child_admin.html', {'form': form},context_instance=RequestContext(request))


def class_view(request, class_id):
    schoolDict={}
    classObj = Class.objects.get(pk=class_id)    
    schoolObj = classObj.sid
    boundaryObj = schoolObj.boundary
    boundaryName = boundaryObj.name
    schoolDict = treeDict(boundaryObj)
    sectionsLis = Sections.objects.filter(classname=classObj, active=1)
    className = classObj.name
    return  render_to_response('class_view.html',{'legend':className, 'schoolDict':schoolDict, 'title':'Class '+str(className), 'entry':'Add', 'boundaryObj':boundaryObj, 'boundary_id':boundaryObj.id, 'classObj':classObj, 'sectionsLis':sectionsLis,'schoolObj':schoolObj})

def class_entry(request, school_id):
    url = '/akshara/class/'+str(school_id)+'/entry/'
    sectionnames = ['%s' %(section[1]) for section in SectionChoices]
    if request.method == 'POST':
        form =Class_Form(request.POST, request.FILES)
        form1 = Section_Form(request.POST, request.FILES)
        if form.is_valid():
	        clasObj = form.save()
	        section = request.POST.getlist('section')
	        for sec in section:
	            secObj = Sections(classname=clasObj, section=sec)
	            secObj.save()
	        return render_to_response('successful.html')
        else:
	        return render_to_response('class_admin.html', {'form': form,'entry':'Add','legend':'Add Class','pagetitle':'Class Form', 'school_id':school_id,'url':url, 'sectionnames':sectionnames},context_instance=RequestContext(request))
    else:
	    form = Class_Form()
	    form1 = Section_Form()
	    return render_to_response('class_admin.html', {'form': form,'entry':'Add','legend':'Add Class','pagetitle':'Class Form','school_id':school_id,'url':url, 'sectionnames':sectionnames},context_instance=RequestContext(request))

def class_edit(request,class_id):
    classobj = Class.objects.get(pk=class_id)
    schoolObj = classobj.sid
    school_id=schoolObj.id
    url = '/akshara/class/'+str(class_id)+'/edit/'
    if request.method == 'POST':
	form =Class_Form(request.POST, request.FILES,instance=classobj)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    else:
    	    form = Class_Form(instance=classobj)
    return render_to_response('class_edit.html', {'form': form,'classobj':classobj,'legend':'Add Class','pagetitle':'Class Form', 'school_id':school_id, 'url':url,},context_instance=RequestContext(request))
       
    
def class_delete(request):
    class_id= request.REQUEST.get('schoolId')   	
    classObj = Class.objects.get(id=class_id)    
    classObj.active=0
    classObj.save()
    return HttpResponse('success')    

def academicyear_entry(request):
    if request.method == 'POST':
	form =AcademicYear_Form(request.POST, request.FILES)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    	else:
    	    form = AcademicYear_Form(request.POST, request.FILES)
    	return render_to_response('academicyear_admin.html', {'form': form,'entry':'Add','legend':'Add Academic Year','pagetitle':'Academic Year Form'},context_instance=RequestContext(request))
    else:
    	    form = AcademicYear_Form()
    return render_to_response('academicyear_admin.html', {'form': form,'entry':'Add','legend':'Add Academic Year','pagetitle':'Academic Year Form'},context_instance=RequestContext(request))
    
def academicyear_edit(request,academicyear_id):
    academicyearobj = Academic_Year.objects.get(pk=academicyear_id)
    if request.method == 'POST':
	form =AcademicYear_Form(request.POST, request.FILES,instance=academicyearobj)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    else:
    	    form = AcademicYear_Form(instance=academicyearobj)
    return render_to_response('academicyear_admin.html', {'form': form},context_instance=RequestContext(request))

def student_entry(request,section_id):
    url = '/akshara/student/'+str(section_id)+'/entry/'
    if request.method == 'POST':
	form =Student_Form(request.POST, request.FILES)
	if form.is_valid():
	    form.save()
    	    return render_to_response('successful.html')
    	else:
    	    form = Student_Form(request.POST, request.FILES)
    	return render_to_response('student_admin.html', {'form': form,'entry':'Add','legend':'Add Student','pagetitle':'Student Form','section_id':section_id,'url':url},context_instance=RequestContext(request))
    else:
    	    form = Student_Form()
    return render_to_response('student_admin.html', {'form': form,'entry':'Add','legend':'Add Student','pagetitle':'Student Form','section_id':section_id,'url':url},context_instance=RequestContext(request))

def student_edit(request,student_id):
    studentobj = student.objects.get(pk=student_id)
    sectionObj = studentobj.class_section
    section_id = sectionObj.id
    url = '/akshara/student/'+str(student_id)+'/edit/'
    if request.method == 'POST':
	form =Student_Form(request.POST, request.FILES,instance=studentobj)
	if form.is_valid():	    
	    form.save()
    	    return render_to_response('successful.html')
    else:        
    	form = Student_Form(instance=studentobj)
    return render_to_response('student_admin.html', {'form': form,'section_id':section_id,'url':url,'studentobj':studentobj},context_instance=RequestContext(request))
    
def student_view(request,student_id):    
    studentobj = student.objects.get(pk=student_id)
    sectionObj = studentobj.class_section
    classObj = sectionObj.classname 
    schoolObj = classObj.sid
    boundaryObj = schoolObj.boundary
    studentName = studentobj.child
    schoolDict = treeDict(boundaryObj)
    return  render_to_response('student_view.html',{'legend':studentName, 'schoolDict':schoolDict, 'title':studentName, 'entry':'Add', 'boundaryObj':boundaryObj, 'boundary_id':boundaryObj.id, 'classObj':classObj, 'sectionObj':sectionObj, 'schoolObj':schoolObj,'studentobj':studentobj}) 
    
def student_delete(request):
    student_id= request.REQUEST.get('schoolId')   	
    studentobj = student.objects.get(pk=student_id)    
    studentobj.active=0
    studentobj.save()
    return HttpResponse('success')     

from pysqlite2 import dbapi2 as sqlite
from django.core import serializers
from django.utils import simplejson


CategoryDic={'cat':Institution_Category,'school_type':Institution_Gender,'moi':Moi_Type,'mgmt':Institution_Management}
def display_info(request):
	key_value = request.GET.get('query')
	fieldName = request.GET.get('fieldName')
	Database = int(request.GET.get('Database'))
	extraParam = int(request.GET.get('extraPram'))
	if Database:
	  connection = sqlite.connect('/home/mahiti/Akshara/Akshara/akshara.db')
	  cursor = connection.cursor()

	  fielfnames = {'boundary':'name','address':'address','school':'name','boundary_type':'boundary_type','child':'firstName'}
	  if extraParam:
	    sectionObj = Sections.objects.get(pk=extraParam)
	    Query = 'select id,%s from schools_%s where boundary_id=%s and %s like "%s%s"'%(fielfnames[fieldName], fieldName, sectionObj.classname.sid.boundary.id, fielfnames[fieldName],key_value,'%')
	  else:   
	    Query = 'select id,%s from schools_%s where %s like "%s%s"'%(fielfnames[fieldName],fieldName,fielfnames[fieldName],key_value,'%')	  
	  cursor.execute(Query)
	  cuisine = cursor.fetchall()
	else:
	    cuisine=CategoryDic[fieldName]
	s={}
	schoolid=[]
	schoolname=[] 
	for i in cuisine:	   
	   if key_value==i[1][:len(key_value)].lower():
		schoolid.append(str(i[0]))
		schoolname.append(str(i[1]))
	s['query']=str(key_value)
	s['suggestions']=schoolname
	s['data']=schoolid
	s['fieldName']='id_'+fieldName
	return HttpResponse(simplejson.dumps(s), content_type='application/json; charset=utf-8')

def Get_info(request):	
	key_value = request.GET.get('query')
	fieldName = request.GET.get('fieldName')
	s={}
	schoolid=[]
	schoolname=[] 
	for i in School_Category:
	     if key_value==i[0][:len(key_value)].lower():
		schoolid.append(str(i[0]))
		schoolname.append(str(i[1]))
	s['query']=str(key_value)
	s['suggestions']=schoolname
	s['data']=schoolid
	s['fieldName']='id_'+fieldName
	return HttpResponse(simplejson.dumps(s), content_type='application/json; charset=utf-8')

