"""
Data format classes ("responders") that can be plugged 
into model_resource.ModelResource and determine how
the objects of a ModelResource instance are rendered
(e.g. serialized to XML, rendered by templates, ...).
"""
from django.core import serializers
from django.core.handlers.wsgi import STATUS_CODE_TEXT
from django.core.paginator import QuerySetPaginator, InvalidPage
# the correct paginator for Model objects is the QuerySetPaginator,
# not the Paginator! (see Django doc)
from django.core.xheaders import populate_xheaders
from django import forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms.util import ErrorDict
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils import simplejson
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.generic.simple import direct_to_template
from django.forms.models import modelformset_factory
from schools.models import *
from schools.forms import *
import datetime

class SerializeResponder(object):
    """
    Class for all data formats that are possible
    with Django's serializer framework.
    """
    def __init__(self, format, mimetype=None, paginate_by=None, allow_empty=False):
        """
        format:
            may be every format that works with Django's serializer
            framework. By default: xml, python, json, (yaml).
        mimetype:
            if the default None is not changed, any HttpResponse calls 
            use settings.DEFAULT_CONTENT_TYPE and settings.DEFAULT_CHARSET
        paginate_by:
            Number of elements per page. Default: All elements.
        """
        self.format = format
        self.mimetype = mimetype
        self.paginate_by = paginate_by
        self.allow_empty = allow_empty
        self.expose_fields = []
        
    def render(self, object_list):
        """
        Serializes a queryset to the format specified in
        self.format.
        """
        # Hide unexposed fields
        hidden_fields = []
        for obj in list(object_list):
            for field in obj._meta.fields:
                if not field.name in self.expose_fields and field.serialize:
                    field.serialize = False
                    hidden_fields.append(field)
        response = serializers.serialize(self.format, object_list)
        # Show unexposed fields again
        for field in hidden_fields:
            field.serialize = True
        return response
    
    def element(self, request, elem):
        """
        Renders single model objects to HttpResponse.
        """
        return HttpResponse(self.render([elem]), self.mimetype)
    
    def error(self, request, status_code, error_dict=None):
        """
        Handles errors in a RESTful way.
        - appropriate status code
        - appropriate mimetype
        - human-readable error message
        """
        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype = self.mimetype)
        response.write('%d %s' % (status_code, STATUS_CODE_TEXT[status_code]))
        if error_dict:
            response.write('\n\nErrors:\n')
            response.write(error_dict.as_text())
        response.status_code = status_code
        return response
    
    def list(self, request, queryset, page=None):
        """
        Renders a list of model objects to HttpResponse.
        """
        if self.paginate_by:
            paginator = QuerySetPaginator(queryset, self.paginate_by)
            if not page:
                page = request.GET.get('page', 1)
            try:
                page = int(page)
                object_list = paginator.page(page).object_list
            except (InvalidPage, ValueError):
                if page == 1 and self.allow_empty:
                    object_list = []
                else:
                    return self.error(request, 404)
        else:
            object_list = list(queryset)
        return HttpResponse(self.render(object_list), self.mimetype)
    
class JSONResponder(SerializeResponder):
    """
    JSON data format class.
    """
    def __init__(self, paginate_by=None, allow_empty=False):
        SerializeResponder.__init__(self, 'json', 'application/json',
                    paginate_by=paginate_by, allow_empty=allow_empty)

    def error(self, request, status_code, error_dict=None):
        """
        Return JSON error response that includes a human readable error
        message, application-specific errors and a machine readable
        status code.
        """
        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype = self.mimetype)
        response.status_code = status_code
        response_dict = {
            "error-message" : '%d %s' % (status_code, STATUS_CODE_TEXT[status_code]),
            "status-code" : status_code,
            "model-errors" : error_dict.as_ul()
        }
        simplejson.dump(response_dict, response)
        return response

class XMLResponder(SerializeResponder):
    """
    XML data format class.
    """
    def __init__(self, paginate_by=None, allow_empty=False):
        SerializeResponder.__init__(self, 'xml', 'application/xml',
                    paginate_by=paginate_by, allow_empty=allow_empty)

    def error(self, request, status_code, error_dict=None):
        """
        Return XML error response that includes a human readable error
        message, application-specific errors and a machine readable
        status code.
        """
        from django.conf import settings
        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype = self.mimetype)
        response.status_code = status_code
        xml = SimplerXMLGenerator(response, settings.DEFAULT_CHARSET)
        xml.startDocument()
        xml.startElement("django-error", {})
        xml.addQuickElement(name="error-message", contents='%d %s' % (status_code, STATUS_CODE_TEXT[status_code]))
        xml.addQuickElement(name="status-code", contents=str(status_code))
        if error_dict:
            xml.startElement("model-errors", {})
            for (model_field, errors) in error_dict.items():
                for error in errors:
                    xml.addQuickElement(name=model_field, contents=error)
            xml.endElement("model-errors")
        xml.endElement("django-error")
        xml.endDocument()
        return response

class TemplateResponder(object):
    """
    Data format class that uses templates (similar to Django's
    generic views).
    """
    def __init__(self, template_dir, paginate_by=None, template_loader=loader,
                 extra_context=None, allow_empty=False, context_processors=None,
                 template_object_name='object', mimetype=None):
        self.template_dir = template_dir
        self.paginate_by = paginate_by
        self.template_loader = template_loader
        if not extra_context:
            extra_context = {}
        for key, value in extra_context.items():
            if callable(value):
                extra_context[key] = value()
        self.extra_context = extra_context
        self.allow_empty = allow_empty
        self.context_processors = context_processors
        self.template_object_name = template_object_name
        self.mimetype = mimetype
        self.expose_fields = None # Set by Collection.__init__
            
    def _hide_unexposed_fields(self, obj, allowed_fields):
        """
        Remove fields from a model that should not be public.
        """
        for field in obj._meta.fields:
            if not field.name in allowed_fields and \
               not field.name + '_id' in allowed_fields:
                obj.__dict__.pop(field.name)    

    def list(self, request, queryset, page=None):
        """
        Renders a list of model objects to HttpResponse.
        """
        template_name = '%s/%s_list.html' % (self.template_dir, queryset.model._meta.module_name)
        if self.paginate_by:
            paginator = QuerySetPaginator(queryset, self.paginate_by)
            if not page:
                page = request.GET.get('page', 1)
            try:
                page = int(page)
                object_list = paginator.page(page).object_list
            except (InvalidPage, ValueError):
                if page == 1 and self.allow_empty:
                    object_list = []
                else:
                    raise Http404
            current_page = paginator.page(page)
            c = RequestContext(request, {
                '%s_list' % self.template_object_name: object_list,
                'is_paginated': paginator.num_pages > 1,
                'results_per_page': self.paginate_by,
                'has_next': current_page.has_next(),
                'has_previous': current_page.has_previous(),
                'page': page,
                'next': page + 1,
                'previous': page - 1,
                'last_on_page': current_page.end_index(),
                'first_on_page': current_page.start_index(),
                'pages': paginator.num_pages,
                'hits' : paginator.count,
            }, self.context_processors)
        else:
            object_list = queryset
            c = RequestContext(request, {
                '%s_list' % self.template_object_name: object_list,
                'is_paginated': False
            }, self.context_processors)
            if not self.allow_empty and len(queryset) == 0:
                raise Http404
        # Hide unexposed fields
        for obj in object_list:
            self._hide_unexposed_fields(obj, self.expose_fields)
        c.update(self.extra_context)        
        t = self.template_loader.get_template(template_name)
        return HttpResponse(t.render(c), mimetype=self.mimetype)

    def element(self, request, elem):
        """
        Renders single model objects to HttpResponse.
        """
        template_name = '%s/%s_detail.html' % (self.template_dir, elem._meta.module_name)
        t = self.template_loader.get_template(template_name)
        c = RequestContext(request, {
            self.template_object_name : elem,
        }, self.context_processors)
        # Hide unexposed fields
        self._hide_unexposed_fields(elem, self.expose_fields)
        c.update(self.extra_context)
        response = HttpResponse(t.render(c), mimetype=self.mimetype)
        populate_xheaders(request, response, elem.__class__, getattr(elem, elem._meta.pk.name))
        return response
    
    def error(self, request, status_code, error_dict=None):
        """
        Renders error template (template name: error status code).
        """
        if not error_dict:
            error_dict = ErrorDict()
        response = direct_to_template(request, 
            template = '%s/%s.html' % (self.template_dir, str(status_code)),
            extra_context = { 'errors' : error_dict },
            mimetype = self.mimetype)
        response.status_code = status_code
        return response
    
    def create_form(self, request, queryset, form_class):
        """
        Render form for creation of new collection entry.
        if not isinstance(form_class, list):
                     form_classes=[form_class]
	             retform=False
        else:
                form_classes=form_class
		retform=True
                retFormlist=[]
	Additional Changes
        1)Passing extra_context to form :
                This is using for to pass parent Ids, and to pass Currently Saving object ids. And to check form save is success or not.
        2)Added if condition (form.is_valid):
                   This is to validate the form submitted.
        
        3)Checking Boundary And Scholl after save:
                  Boundary Checking:
                  1.If the Boundary name is same and aboundary category is distict then it will create boundary type relation with existing boundary.
                  2.If the Boundary created is lower level (Cluster or Circle). Then it will refer top most parent of parent of particular boundary . This is usefull to filter boundaries easily in assessment entry link.
 			School Checking:
1.If the School is Anganwadi then it creates class automatically.
			StudentGroup Checking:
			      1. Here we will check where to add school group to school are boundary
        
        4)Checking Button type:
			Save:
				If button type is Save then the page redirects to view page.
			Save And Continue:
				If button type is Save and Continue it redirects to edit page.
			Save And Add Another:
				If button type is Save and Add Another thean page will add new form.

       5)And form = ResourceForm() is changed to form = ResourceForm(queryset=form_class.objects.none()) .
                      This is to get only one form . Other wise it gives the all the forms which has same model name.
       MultiForms:

          6)If we have more than one form we will send fom Api as a list of forms.
             There we assign it to like this
             ResourceForm = modelformset_factory(Child) 
             ResourceForm1 = modelformset_factory(Relations)
             Here we use 2 and 3 forms, so if two forms we do like mentioned above 
             if 3 forms we check for  condition 
                     if len(form_class)!= 2:
                     ResourceForm2 = modelformset_factory(Student)
          7)If request.POST:
                 We save the content 
		     Save:
			If button type is Save then the page redirects to view page.
		     Save And Continue:
			If button type is Save and Continue it redirects to edit page.
		     Save And Add Another:
			If button type is Save and Add Another thean page will add new form.

        """ 
	ResourceForm = modelformset_factory(queryset.model,form=form_class)
	self.extra_context['showsuccess']=False
	if  request.POST.get('replaceTrue',None)==None:
	        self.extra_context['replaceTrue'] = True
	else:
               self.extra_context['replaceTrue'] = False
	 
	if request.POST:
	  	form = ResourceForm(request.POST)
	  	Valid=form.is_valid()
		RelationValid=True
		ChildTrue=queryset.model._meta.module_name=='child' and True or False
		if  ChildTrue:
			if not (request.POST.get('form-0-fatherfirstname','') or request.POST.get('form-0-motherfirstname','')):
				RelationValid=False
				Valid=False
				
		if form_class == Institution_Form:
			if request.POST.get('form-0-address') and request.POST.get('form-0-languages') and request.POST.get('form-0-name'):
				addressObj = Institution_address(address=request.POST.get('form-0-address'), area = request.POST.get('form-0-area'), pincode = request.POST.get('form-0-pincode'), instidentification = request.POST.get('form-0-instidentification'), landmark = request.POST.get('form-0-landmark'), routeInformation = request.POST.get('form-0-routeInformation'))
				addressObj.save()
				Valid = True		
	  	if Valid:
	  		if form_class == Institution_Form:
				new_data = request.POST.copy()
	  			new_data['form-0-inst_address'] = addressObj.id
				form = ResourceForm(new_data)
				obj = form.save()[0]
				boundaryObj = Boundary.objects.get(pk=request.POST.get('form-0-boundary'))
				
				if boundaryObj.boundary_category.boundary_category.lower() == 'circle' and boundaryObj.boundary_type.boundary_type.lower() =='anganwadi':
					newClass = StudentGroup(name="Anganwadi Class", active=2, institution_id=obj.id)
					newClass.save()
			elif form_class == Staff_Form:
				obj = form.save()[0]
				classes = request.POST.getlist('form-0-student_group')
				for clas in classes:
					studGrupObj = StudentGroup.objects.get(pk=clas)
					relObj = Staff_StudentGroupRelation(staff=obj, student_group=studGrupObj, academic=current_academic(), active=2)
					relObj.save()		
	  		else:
				obj = form.save()[0]
				if queryset.model._meta.module_name=='child':
					relation = {'form-0-motherfirstname':'Mother','form-0-fatherfirstname':'Father'}
					names = {'Mother-MiddleName':'form-0-mothermiddlename','Mother-LastName':'form-0-motherlastname','Father-MiddleName':'form-0-fathermiddlename', 'Father-LastName':'form-0-fatherlastname'}
					for rel_type,rel_value in relation.iteritems():
						if request.POST[rel_type]:
							relation=Relations(relation_type=rel_value,first_name=request.POST[rel_type], middle_name=request.POST[names[rel_value+'-MiddleName']], last_name=request.POST[names[rel_value+'-LastName']], child=obj)
							relation.save()
	  			

			buttonType = str(self.extra_context['buttonType'])
			self.extra_context['showsuccess']=True
			
			if buttonType == 'save':
				respDict = {queryset.model._meta.module_name.lower():obj,'showsuccess':True}
				
				'''if queryset.model._meta.module_name == "studentgroup":
					stdgrp = StudentGroup.objects.get(id=obj.id)
					if stdgrp.content_type.model == "institution":
						school = Institution.objects.get(id = stdgrp.object_id)
						studgrpParent = school
					else:
						boundary = Boundary.objects.get(id = stdgrp.object_id)
						studgrpParent = boundary
					respDict['studgrpParent'] = studgrpParent'''
				if queryset.model._meta.module_name=='child':
				    if request.POST['ModelName']=="student":
					respDict['student'] = True
					student = Student(child=obj, otherStudentId=request.POST.get('form-0-otherId'), active=2)
					student.save()
					std_stdgrp_relation = Student_StudentGroupRelation(student=student,student_group=self.extra_context['studentgroup'],academic=current_academic(),active=2)
					std_stdgrp_relation.save()
					if self.extra_context['mapStudent'] in [1 , '1']:
						assessmentObj = Assessment.objects.get(pk=self.extra_context['assessment_id'])
						questions_list = Question.objects.filter(assessment = assessmentObj, active=2)
						entryStr = '''<tr class='KLP_txt_cen'><td><form onsubmit='return false;' id='id_Student_%s' name='student_%s' class="validForm"><input type='hidden' value='%s' name='programId'><input type='hidden' value='%s' name='assessmentId'><input type='hidden' value='%s' name='student'><input type='hidden' value='%s' name='student_groupId'><table><tbody><tr>''' %(student.id, student.id, assessmentObj.programme.id, self.extra_context['assessment_id'], student.id, self.extra_context['studentgroup_id'])
						for question in questions_list:
							qType = 'digits'
							if question.questionType == 2:
								qType = 'letters'
							
							entryStr = entryStr + '''<td class='KLP_td_height'><input type='text' class='required %s' size='3' value='' id='id_student_%s_%s' name='student_%s_%s' tabindex='1'></td>''' %(qType, student.id, question.id, student.id, question.id)
						entryStr = entryStr + '''<td class='KLP_td_height'> <input type='submit' value='submit' formname='id_Student_%s' url='/answer/data/entry/' tabindex='1'><script>$().ready(function() {KLP_validateScript("id_Student_%s");});</script></td></tr></tbody></table></form></td></tr>''' %(student.id, student.id)
						detailStr = '''<tr class='KLP_txt_cen'><td><table><tr><td class='KLP_td_width'>%s</td><td class='KLP_td_width'><span class='blue' title='Father: %s, Mother: %s, Gender: %s, MT: %s, DOB: %s'>%s&nbsp;%s</span><span class='KLP_Form_status' id='id_Student_%s_status'>Form Status</span></td></tr></table></td></tr>''' %(student.id, request.POST['form-0-fatherfirstname'], request.POST['form-0-motherfirstname'], student.child.gender, student.child.mt, student.child.dob.strftime("%d-%m-%Y"), student.child.firstName, student.child.lastName, student.id)
						mapStudenStr = {'detailStr':detailStr, 'ansEntryStr':entryStr}
						return HttpResponse(simplejson.dumps(mapStudenStr), content_type='application/json; charset=utf-8')

				template_name = '%s/%s_detail.html' % (self.template_dir, queryset.model._meta.module_name)
                		response = render_to_response(template_name, respDict)
                		return response
                	elif buttonType == 'save and continue':
                		elem = queryset.get(**{queryset.model._meta.pk.name : obj.id})
                		ResourceForm = modelformset_factory(queryset.model, extra=0)
                		form = ResourceForm(queryset=queryset.model.objects.filter(pk=obj.id))
                		template_name = '%s/%s_form.html' % ('edittemplates', elem._meta.module_name)
        			return render_to_response(template_name, {'form':form, 'update':True, self.template_object_name:elem, 'extra_context':self.extra_context})
			elif buttonType == 'save and add another':
				self.extra_context['prevousId'] = obj.id
				if form_class == Question_Form:
					self.extra_context['order'] = len(Question.objects.filter(assessment__id=self.extra_context['referKey']))+1
				form = ResourceForm(queryset=queryset.model.objects.none())
			else:
				if form_class in [Institution_Category_Form, Moi_Type_Form, Institution_Management_Form]:	
					response = "<input type=hidden id=success_status size=15 value=True /><input type=hidden value=%s id=obj_id />" %(obj.id)
					return response
				return obj
					
		else:
			form = 	ResourceForm(request.POST)
			if not RelationValid:
				form.errors[0]['first_name']=['Any of these fields is required.']
			template_name = '%s/%s_form.html' % (self.template_dir, queryset.model._meta.module_name)
			response = render_to_response(template_name, {'form':form,'extra_context':self.extra_context })
			return response
		
	else:
		form = ResourceForm(queryset=queryset.model.objects.none())
	
	
	template_name = '%s/%s_form.html' % (self.template_dir, queryset.model._meta.module_name)
	return render_to_response(template_name, {'form':form,'extra_context':self.extra_context })

    def update_form(self, request, pk, queryset, form_class):
        """
        Render edit form for single entry.

        Update_form:
            1)Changed ResourceForm = forms.form_for_instance(elem, form=form_class) to ResourceForm = modelformset_factory(queryset.model, extra=0) .To get Only One Form.

            2)forms.form_for_instance changed to  modelformset_factory. Because it is not supporting form_for_instance.

            3)Using  request.POST instead of request.PUT
			request is not supporting PUT.

            4)Added if form_is_valid(): This is to vaidate the form.

            5)If form is submitted without changing data then it throws an error. So using try except to avoid exception.
            6)Passing extra_context to form :
                   This is using for to pass parent Ids, and to pass Currently Saving object ids. And to check form save is success or not.

            7)Checking Button type:
			Save:
				If button type is Save then the page redirects to view page.
			Save And Continue:
				If button type is Save and Continue it redirects to edit page.
			Save And Add Another:
				If button type is Save and Add Another thean page will add new form.
           MultiForms Update:
	         1) If we have more than one form we will send fom Api as a list of forms.
                              There we assign it to like this
                              ResourceForm = modelformset_factory(Child , extra=0) 
                              ResourceForm1 = modelformset_factory(Relations, extra=0)
                              Here we use 2 and 3 forms, so if two forms we do like mentioned above 
                              if 3 forms we check for  condition 
                              if len(form_class)!= 2:
			         ResourceForm2 = modelformset_factory(Student, extra=0)
	        2)  If request.POST:
		             Here  we need to mention pk value

		             form = ResourceForm2(new_data, queryset=Student.objects.filter(pk=pk), )
		             Now it knows which data is edited.

                            Then we save the content 
		            Save:
			          If button type is Save then the page redirects to view page.
		           Save And Continue:
			           Here we will send all forms to edit.
			      If button type is Save and Continue it redirects to edit page.
		          Save And Add Another:
			        After saveing content we will fresh forms to add one more record.
			        If button type is Save and Add Another thean page will add new form.
        """
        # Remove queryset cache by cloning the queryset
        #queryset = queryset._clone()
        elem = queryset.get(**{queryset.model._meta.pk.name : pk})
        #ResourceForm = forms.form_for_instance(elem, form=form_class)
	ResourceForm = modelformset_factory(queryset.model,form=form_class, extra=0)
	self.extra_context['showsuccess']=False
	if  request.POST.get('replaceTrue',None)==None:
	        self.extra_context['replaceTrue'] = True
	else:
               self.extra_context['replaceTrue'] = False

	if request.POST:
		form = ResourceForm(request.POST, queryset=queryset.model.objects.filter(pk=pk), )
		Valid=form.is_valid()
		RelationValid=True
		ChildTrue=queryset.model._meta.module_name=='child' and True or False
		if  ChildTrue:
			if not (request.POST.get('form-0-fatherfirstname','') or request.POST.get('form-0-motherfirstname','')):
				RelationValid=False
				Valid=False
		if queryset.model._meta.module_name == 'institution':
			if request.POST.get('form-0-address') and request.POST.get('form-0-languages') and request.POST.get('form-0-name'):
				addressObj = elem.inst_address
				addressObj.address = request.POST.get('form-0-address')
				addressObj.area = request.POST.get('form-0-area')
				addressObj.pincode = request.POST.get('form-0-pincode')
				addressObj.instidentification = request.POST.get('form-0-instidentification')
				addressObj.landmark = request.POST.get('form-0-landmark')
				addressObj.routeInformation = request.POST.get('form-0-routeInformation')
				addressObj.save()
				Valid = True			
		if Valid:
			'''try:
				obj = form.save()[0]
			except:
				obj = queryset.model.objects.get(pk=pk)'''
			if queryset.model._meta.module_name=='institution':
				new_data = request.POST.copy()
				new_data['form-0-inst_address'] = addressObj.id	
				form = ResourceForm(new_data, queryset=queryset.model.objects.filter(pk=pk),)
				obj = form.save()[0]		
			else:	
				form.save()
				obj = queryset.model.objects.get(pk=pk)
			if queryset.model._meta.module_name=='child':
				studObj = obj.getStudent()
				studObj.otherStudentId = request.POST.get('form-0-otherId')
				studObj.save()
				relation = {'form-0-motherfirstname':'Mother','form-0-fatherfirstname':'Father'}
				names = {'Mother-MiddleName':'form-0-mothermiddlename','Mother-LastName':'form-0-motherlastname','Father-MiddleName':'form-0-fathermiddlename', 'Father-LastName':'form-0-fatherlastname'}
				for rel_type,rel_value in relation.iteritems():
					if request.POST[rel_type]:
						relation=Relations.objects.filter(relation_type=rel_value,child=obj).update(first_name=request.POST[rel_type], middle_name=request.POST[names[rel_value+'-MiddleName']], last_name=request.POST[names[rel_value+'-LastName']])
			elif queryset.model._meta.module_name=='staff':
				mappedClasses = elem.getAssigendClasses()
				mapClasIds = []
				classes = request.POST.getlist("form-0-student_group")
				newclasses = [int(i) for i in classes]
				for mapClas in mappedClasses:
					mapClasIds.append(mapClas.id)
					if mapClas.id not in newclasses:
						
						staff_StudentGroup = Staff_StudentGroupRelation.objects.filter(staff__id = pk, student_group = mapClas, academic=current_academic(),)[0]
						staff_StudentGroup.active = 1 
						staff_StudentGroup.save()
				
				for clas in newclasses:
					if clas not in mapClasIds:
						clasObj = StudentGroup.objects.get(pk=clas)
						staff_StudentGroup = Staff_StudentGroupRelation(staff = elem, student_group = clasObj, academic=current_academic())
						staff_StudentGroup.save()			

			buttonType = str(self.extra_context['buttonType'])
			self.extra_context['showsuccess']=True
			if buttonType == 'save':
				respDict = {elem._meta.module_name.lower():obj,'showsuccess':True,}
				if queryset.model._meta.module_name=='child':
					if request.POST['ModelName']=="student":
						respDict['student'] = True
				'''if queryset.model._meta.module_name == "studentgroup":
					stdgrp = StudentGroup.objects.get(id=obj.id)
					if stdgrp.content_type.model == "school":
						school = School.objects.get(id = stdgrp.object_id)
						studgrpParent = school
					else:
						boundary = Boundary.objects.get(id = stdgrp.object_id)
						studgrpParent = boundary
					respDict['studgrpParent'] = studgrpParent'''
				if form_class == Staff_Form:
					template_name = '%s/%s_detail.html' % ('edittemplates', elem._meta.module_name)
				else:
					template_name = '%s/%s_detail.html' % ('viewtemplates', elem._meta.module_name)
                		response = render_to_response(template_name, respDict)
                		return response	
                	elif  buttonType == 'save and continue':
                		retFormlist = ResourceForm(queryset=queryset.model.objects.filter(pk=obj.id))
                	elif buttonType == 'save and add another':
                		self.extra_context['prevousId'] = obj.id
                		if form_class == Question_Form:
					self.extra_context['order'] = len(Question.objects.filter(assessment__id=self.extra_context['referKey']))+1
                		ResourceForm = modelformset_factory(queryset.model, form=form_class,)
                		form = ResourceForm(queryset=queryset.model.objects.none())
                		template_name = '%s/%s_form.html' % ('viewtemplates', elem._meta.module_name)
				response = render_to_response(template_name, {'form':form,'extra_context':self.extra_context })
				return response
                			
			
		else:
			
			form = 	ResourceForm(request.POST)
			if not RelationValid:
				form.errors[0]['first_name']=['Any of these fields is required.']
			template_name = '%s/%s_form.html' % (self.template_dir, elem._meta.module_name)
			return render_to_response(template_name, {'form':form, 'update':True, self.template_object_name:elem, 'extra_context':self.extra_context})
			
	else:
		form = ResourceForm(queryset=queryset.model.objects.filter(pk=pk))
	
        template_name = '%s/%s_form.html' % (self.template_dir, elem._meta.module_name)
        #print template_name
        #print 'cccccccccccccc'
        return render_to_response(template_name, 
                {'form':form, 'update':True, self.template_object_name:elem, 'extra_context':self.extra_context})
