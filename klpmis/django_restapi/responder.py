#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import  simplejson
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.generic import TemplateView
from django.forms.models import modelformset_factory
from schools.models import *
from schools.forms import *
import datetime
from django.db import transaction


class SerializeResponder(object):

    """
    Class for all data formats that are possible
    with Django's serializer framework.
    """

    def __init__(
        self,
        format,
        mimetype=None,
        paginate_by=None,
        allow_empty=False,
        ):
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
                if not field.name in self.expose_fields \
                    and field.serialize:
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

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Handles errors in a RESTful way.
        - appropriate status code
        - appropriate mimetype
        - human-readable error message
        """

        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype=self.mimetype)
        response.write('%d %s' % (status_code,
                       STATUS_CODE_TEXT[status_code]))
        if error_dict:
            response.write('''

Errors:
''')
            response.write(error_dict.as_text())
        response.status_code = status_code
        return response

    def list(
        self,
        request,
        queryset,
        page=None,
        ):
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
                                    paginate_by=paginate_by,
                                    allow_empty=allow_empty)

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Return JSON error response that includes a human readable error
        message, application-specific errors and a machine readable
        status code.
        """

        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype=self.mimetype)
        response.status_code = status_code
        response_dict = {'error-message': '%d %s' % (status_code,
                         STATUS_CODE_TEXT[status_code]),
                         'status-code': status_code,
                         'model-errors': error_dict.as_ul()}
        simplejson.dump(response_dict, response)
        return response


class XMLResponder(SerializeResponder):

    """
    XML data format class.
    """

    def __init__(self, paginate_by=None, allow_empty=False):
        SerializeResponder.__init__(self, 'xml', 'application/xml',
                                    paginate_by=paginate_by,
                                    allow_empty=allow_empty)

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Return XML error response that includes a human readable error
        message, application-specific errors and a machine readable
        status code.
        """

        from django.conf import settings
        if not error_dict:
            error_dict = ErrorDict()
        response = HttpResponse(mimetype=self.mimetype)
        response.status_code = status_code
        xml = SimplerXMLGenerator(response, settings.DEFAULT_CHARSET)
        xml.startDocument()
        xml.startElement('django-error', {})
        xml.addQuickElement(name='error-message', contents='%d %s'
                            % (status_code,
                            STATUS_CODE_TEXT[status_code]))
        xml.addQuickElement(name='status-code',
                            contents=str(status_code))
        if error_dict:
            xml.startElement('model-errors', {})
            for (model_field, errors) in error_dict.items():
                for error in errors:
                    xml.addQuickElement(name=model_field,
                            contents=error)
            xml.endElement('model-errors')
        xml.endElement('django-error')
        xml.endDocument()
        return response


class TemplateResponder(object):

    """
    Data format class that uses templates (similar to Django's
    generic views).
    """

    def __init__(
        self,
        template_dir,
        paginate_by=None,
        template_loader=loader,
        extra_context=None,
        allow_empty=False,
        context_processors=None,
        template_object_name='object',
        mimetype=None,
        ):

        self.template_dir = template_dir
        self.paginate_by = paginate_by
        print extra_context
        self.template_loader = template_loader
        if not extra_context:
            extra_context = {}
        for (key, value) in extra_context.items():
            if callable(value):
                extra_context[key] = value()
        self.extra_context = extra_context
        print 'eeeee', self.extra_context, extra_context, \
            'EEEEEEEEEEEEEEEEEEEEEe'
        self.allow_empty = allow_empty
        self.context_processors = context_processors
        self.template_object_name = template_object_name
        self.mimetype = mimetype
        self.expose_fields = None  # Set by Collection.__init__

    def _hide_unexposed_fields(self, obj, allowed_fields):
        """
        Remove fields from a model that should not be public.
        """

        for field in obj._meta.fields:
            if not field.name in allowed_fields and not field.name \
                + '_id' in allowed_fields:
                obj.__dict__.pop(field.name)

    def list(
        self,
        request,
        queryset,
        page=None,
        ):
        """
        Renders a list of model objects to HttpResponse.
        """

        template_name = '%s/%s_list.html' % (self.template_dir,
                queryset.model._meta.module_name)
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
                'hits': paginator.count,
                }, self.context_processors)
        else:
            object_list = queryset
            c = RequestContext(request, {'%s_list' \
                               % self.template_object_name: object_list,
                               'is_paginated': False},
                               self.context_processors)
            if not self.allow_empty and len(queryset) == 0:
                raise Http404

        # Hide unexposed fields

        print 'hssssssssdddddd', c
        for obj in object_list:
            self._hide_unexposed_fields(obj, self.expose_fields)
        c.update(self.extra_context)
        print self.extra_context, 'in resp'
        t = self.template_loader.get_template(template_name)
        return HttpResponse(t.render(c), mimetype=self.mimetype)

    def element(self, request, elem):
        """
        Renders single model objects to HttpResponse.
        """

        template_name = '%s/%s_detail.html' % (self.template_dir,
                elem._meta.module_name)
        t = self.template_loader.get_template(template_name)
        c = RequestContext(request, {self.template_object_name: elem},
                           self.context_processors)

        # Hide unexposed fields

        self._hide_unexposed_fields(elem, self.expose_fields)
        c.update(self.extra_context)
        response = HttpResponse(t.render(c), mimetype=self.mimetype)
        populate_xheaders(request, response, elem.__class__,
                          getattr(elem, elem._meta.pk.name))
        return response

    def error(
        self,
        request,
        status_code,
        error_dict=None,
        ):
        """
        Renders error template (template name: error status code).
        """

        if not error_dict:
            error_dict = ErrorDict()
        response = TemplateView.as_view (request, template='%s/%s.html'
                % (self.template_dir, str(status_code)),
                extra_context={'errors': error_dict},
                mimetype=self.mimetype)
        response.status_code = status_code
        return response

    # @transaction.commit_manually

    def create_form(
        self,
        request,
        queryset,
        form_class,
        ):
        """  Render form for creation of new collection entry. """

        ResourceForm = modelformset_factory(queryset.model,
                form=form_class)  # get model formset factory based on model and form
        #print ResourceForm()

        self.extra_context['showsuccess'] = False  # Pass showsuccess True or false for message
        if request.POST.get('replaceTrue', None) == None:
            self.extra_context['replaceTrue'] = True
        else:
            self.extra_context['replaceTrue'] = False
        answerAddable = False
        DefaultAnswer = True
        if queryset.model._meta.module_name.lower() == 'question':
            Assobj = \
                Assessment.objects.get(id=self.extra_context['referKey'
                    ])
            print Assobj, Assobj.getAssessmentStatus, 'status'
            if Assobj.getAssessmentStatus() and Assobj.flexi_assessment:
                answerAddable = True
        self.extra_context['answerAddable'] = answerAddable
        print 'ASSSSSSSSSSSS', queryset.model._meta.module_name.lower()
        if request.POST:

        # If request method is post, post data
          # form = ResourceForm(request.POST) # post data to form
          # Valid=form.is_valid()  # Validate form

            RelationValid = True
            IValid = True
            print request.POST
            new_data = request.POST.copy()
            modulename = queryset.model._meta.module_name

        # Check if current model is child then pass ChildTrue to True else false

            ChildTrue = modulename == 'child' and True or False
            AssValid = True
            ''' 
            if ChildTrue:

            # Check for realtion names if names are not there validation fail
                
                if not (request.POST.get('form-0-fatherfirstname', '')
                        or request.POST.get('form-0-motherfirstname', ''
                        )):
                
                     RelationValid = False #Relationform.is_valid()

                # IValid=False
            '''
            print ChildTrue
            if form_class == Assessment_Form:
                print 'SSSSSSSSSS'
                if request.POST.get('form-0-flexi_assessment'):
                    print request.POST.get('form-0-flexi_assessment')
                    if not request.POST.get('form-0-primary_field_name'
                            ) \
                        or not request.POST.get('form-0-primary_field_type'
                            ):

                        AssValid = False
            if form_class == Question_Form and answerAddable:
                if request.POST.get('defaultanswer', 'a').lower() \
                    not in ['uk', 'ab']:
                    DefaultAnswer = False
            if request.POST.get('defaultanswer'):
                self.extra_context['defaultanswer'] = \
                    request.POST.get('defaultanswer')
            if form_class == Institution_Form:

            # If Institution Check for address information save data

                if request.POST.get('form-0-address') \
                    and request.POST.get('form-0-languages') \
                    and request.POST.get('form-0-name'):
                    addressObj = Institution_address(
                        address=request.POST.get('form-0-address'),
                        area=request.POST.get('form-0-area'),
                        pincode=request.POST.get('form-0-pincode'),
                        instidentification=request.POST.get('form-0-instidentification'
                                ),
                        landmark=request.POST.get('form-0-landmark'),
                        route_information=request.POST.get('form-0-route_information'
                                ),
                        )
                    addressObj.save()
                    new_data['form-0-inst_address'] = addressObj.id
                    IValid = True
                else:
                    IValid = False
            form = ResourceForm(new_data,request)  # post data to form
            Valid = form.is_valid()  # Validate form
            qvalid = True
            print Valid,'Valid',form.errors
            if Valid and IValid and qvalid and AssValid \
                and DefaultAnswer and RelationValid:

              # If From is valid then save data

                if form_class == Institution_Form:

                # new_data = request.POST.copy()
                                # addressObj.save()
                  # new_data['form-0-inst_address'] = addressObj.id
                  # pass address id to the institution to save data
                # form = ResourceForm(new_data)

                    if 1:
                        obj = form.save()[0]  # save data................
                    else:

                        addressObj.delete()
                    print 'OBK'
                    boundaryObj = \
                        Boundary.objects.get(pk=request.POST.get('form-0-boundary'
                            ))
                    userob = User.objects.filter(id=request.user.id)[0]
                    userob.set_perms(['Acess'], obj)
                    print boundaryObj.boundary_category.boundary_category.lower(), \
                        boundaryObj.boundary_type.boundary_type.lower()
                    if boundaryObj.boundary_category.boundary_category.lower() \
                        == 'circle' \
                        and boundaryObj.boundary_type.boundary_type.lower() \
                        in ['anganwadi', 'preschool']:

                    # if boundary category is circle and boundary type is anganwadi create a class with name Anganwadi Class

                        print 'inside IF'
                        newClass = StudentGroup(name='Anganwadi Class',
                                active=2, institution_id=obj.id,
                                group_type='Class')
                        newClass.save()
                elif form_class == Staff_Form:

                # If Staff save data for staff and create relation with SG

                    obj = form.save()[0]
                    classes = \
                        request.POST.getlist('form-0-student_group')
                    for clas in classes:
                        studGrupObj = StudentGroup.objects.get(pk=clas)
                        relObj = Staff_StudentGroupRelation(staff=obj,
                                student_group=studGrupObj,
                                academic=current_academic(), active=2)
                        relObj.save()
                elif modulename == 'studentgroup':
                    grouptype = request.POST.get('form-0-group_type')
                    active = request.POST.get('form-0-active')
                    instutionid = request.POST.get('form-0-institution')
                    section = request.POST.get('form-0-section')
                    name = request.POST.get('form-0-name')
                    print 'studentgroupsssssssssssssssss'
                    obj = form.save()[0] 
                    '''StudentGroup(group_type=grouptype,
                            active=active, institution_id=instutionid,
                            section=section, name=name)
                    obj.save()
                    '''
                    '''
                    elif modulename == 'child':
                    firstname = request.POST.get('form-0-first_name')
                    middlename = request.POST.get('form-0-middle_name')
                    lastname = request.POST.get('form-0-last_name')
                    uid = request.POST.get('form-0-uid')
                    mt = request.POST.get('form-0-mt')
                    gender = request.POST.get('form-0-gender')
                    dob = \
                        datetime.date(int(request.POST.get('form-0-dob_year'
                            )), int(request.POST.get('form-0-dob_month'
                            )), int(request.POST.get('form-0-dob_day')))
                    obj = Child(
                        first_name=firstname,
                        last_name=lastname,
                        middle_name=middlename,
                        uid=uid,
                        mt_id=mt,
                        gender=gender,
                        dob=dob,
                        )
                    #obj.save()
                    form.save()
                    '''
                else:

                  # else save data

                    obj = form.save()[0]
                    print 'OBJECT', obj.id
                '''
                if modulename == 'child':

                    # If current model is child save relations data.
                   
                    relation = {'form-0-motherfirstname': 'Mother',
                                'form-0-fatherfirstname': 'Father'}
                    names = {
                        'Mother-MiddleName': 'form-0-mothermiddlename',
                        'Mother-LastName': 'form-0-motherlastname',
                        'Father-MiddleName': 'form-0-fathermiddlename',
                        'Father-LastName': 'form-0-fatherlastname',
                        }
                    
                    for (rel_type, rel_value) in relation.iteritems():
                        if request.POST[rel_type]:
                            relation = \
                                Relations(relation_type=rel_value,
                                    first_name=request.POST[rel_type],
                                    middle_name=request.POST[names[rel_value
                                    + '-MiddleName']],
                                    last_name=request.POST[names[rel_value
                                    + '-LastName']], child=obj)
                            relation.save()
                '''    
                if modulename == 'question':

                    # If current model is child save relations data.

                    defaultanswer = request.POST.get('defaultanswer', ''
                            )
                    if Assobj.flexi_assessment and defaultanswer:
                        Question_List = \
                            Question.objects.filter(assessment=Assobj)
                        AnsObjs = \
                            Answer.objects.filter(question__in=Question_List).distinct('flexi_data'
                                )
                        answerStatus = -99999
                        if defaultanswer.lower() == 'uk':
                            answerStatus = -1
                        for AnsObj in AnsObjs:
                            AnsObj.id = None
                            AnsObj.question_id = obj.id
                            AnsObj.status = answerStatus
                            AnsObj.answer_score = None
                            AnsObj.anserGrade = None
                            AnsObj.save()
                            print 'AnsObj', AnsObj.id
                buttonType = str(self.extra_context['buttonType'])  # get button type
                self.extra_context['showsuccess'] = True  # make showsuccess is True

                if buttonType == 'save':

                # If Button type is Save

                    respDict = {modulename.lower(): obj,
                                'showsuccess': True}

                    if modulename == 'child':
	                     if request.POST['form-0-ModelName'] == 'student':

				    # if current model is Chils and ModelName is Student

				    respDict['student'] = True
				    #Move into forms.py
				    ''' 
				    # Create Student Object With as foreign key
					    
					    student = Student.objects.get(child=obj,
					            other_student_id=request.POST.get('form-0-otherId'
					            ), active=2)
					    #student.save()
					    
				    # Create relation ship with SG for current academic year.
					    
					    #std_stdgrp_relation = \
					    #    Student_StudentGroupRelation(student=student,
					    #        student_group=self.extra_context['studentgroup'
					    #        ], academic=current_academic(),
					    #        active=2)

					    #std_stdgrp_relation.save()
				     '''                        
		                    totallengthstudent = \
		                        Student_StudentGroupRelation.objects.filter(student_group=self.extra_context['studentgroup'
		                            ], academic=current_academic(),
		                            active=2).count()
		                    if self.extra_context['mapStudent'] in [1,
		                            '1']:

				        	# mapstudent has value 1 add row in the assessment data entry screen.

				                assessmentObj = \
				                    Assessment.objects.get(pk=self.extra_context['assessment_id'
				                        ])
				                questions_list = \
				                    Question.objects.filter(assessment=assessmentObj,
				                        active=2)
				                entryStr = \
				                    '''<tr class='KLP_txt_cen'><td><form onsubmit='return false;' id='id_Student_%s' name='student_%s' class="validForm"><div style="display: none;"><input type="hidden" value="%s" name="csrfmiddlewaretoken"></div><input type='hidden' value='%s' name='programId'><input type='hidden' value='%s' name='assessmentId'><input type='hidden' value='%s' name='student'><input type='hidden' value='%s' name='student_groupId'><input type="hidden" name="formcounter" id="formcounter" value="%s"><table><tbody><tr>''' \
				                    % (
				                    student.id,
				                    student.id,
				                    request.META.get('CSRF_COOKIE',
			None),
				                    assessmentObj.programme.id,
				                    self.extra_context['assessment_id'
			],
				                    student.id,
				                    self.extra_context['studentgroup_id'
			],
				                    totallengthstudent,
				                    )
				                for question in questions_list:
				                    if question.question_type == 1:
				                        entryStr = entryStr \
		    + '''<td class='KLP_td_height'><span style="color:#736F6E;">%s</span><br/><input type='text' class='required digits' size='3' value='' id='id_student_%s_%s' name='student_%s_%s_%s' tabindex='1' min="%s" max="%s"></td>''' \
		    % (
				                            question.order,
				                            student.id,
				                            question.id,
				                            student.id,
				                            question.id,
				                            totallengthstudent,
				                            question.score_min,
				                            question.score_max,
				                            )
				                    else:
				                        entryStr = entryStr \
		    + '''<td class='KLP_td_height'><span style="color:#736F6E;">%s</span><br/><input type='text' class='required' size='3' value='' id='id_student_%s_%s' name='student_%s_%s_%s' tabindex='1' isinGrades="%s"></td>''' \
		    % (
				                            question.order,
				                            student.id,
				                            question.id,
				                            student.id,
				                            question.id,
				                            totallengthstudent,
				                            question.grade,
				                            )
				                entryStr = entryStr \
				                    + '''<td class='KLP_td_height'> <input type='submit' value='submit' formname='id_Student_%s' url='/answer/data/entry/' tabindex='1'><script>$().ready(function() {KLP_validateScript("id_Student_%s");});</script></td></tr></tbody></table></form></td></tr>''' \
				                    % (student.id, student.id)
				                detailStr = \
				                    '''<tr class='KLP_txt_cen'><td><table><tr><td class='KLP_td_width'>%s</td><td class='KLP_td_width'><span class='blue' title='Father: %s, Mother: %s, Gender: %s, MT: %s, DOB: %s'>%s&nbsp;%s</span><span class='KLP_Form_status' id='id_Student_%s_status'>Form Status</span></td></tr></table></td></tr>''' \
				                    % (
				                    student.id,
				                    request.POST['form-0-fatherfirstname'
			],
				                    request.POST['form-0-motherfirstname'
			],
				                    student.child.gender,
				                    student.child.mt,
				                    student.child.dob.strftime('%d-%m-%Y'
			),
				                    student.child.first_name,
				                    student.child.last_name,
				                    student.id,
				                    )
				                mapStudenStr = {'detailStr': detailStr,
				                        'ansEntryStr': entryStr}
				                return HttpResponse(simplejson.dumps(mapStudenStr),
				                        content_type='application/json; charset=utf-8'
				                        )

                    # Show detail about newly create Object........

                    template_name = '%s/%s_detail.html' \
                        % (self.template_dir, modulename)
                    response = render_to_response(template_name,
                            respDict,
                            context_instance=RequestContext(request))
                    return response
                elif buttonType == 'save and continue':

                        # If buttonType is save and continue show edit form for the object
                    if modulename.lower() in ['staff','assessment_lookup']:
        
                       self.extra_context['replaceTrue']=False
                    elem = \
                        queryset.model.objects.get(**{queryset.model._meta.pk.name: obj.id})
                    ResourceForm = modelformset_factory(queryset.model,
                            extra=0)
                    form = \
                        ResourceForm(queryset=queryset.model.objects.filter(id=obj.id))
                    template_name = '%s/%s_form.html' % ('edittemplates'
                            , modulename)
                    return render_to_response(template_name, {
                        'form': form,
                        'update': True,
                        self.template_object_name: elem,
                        'extra_context': self.extra_context,
                        }, context_instance=RequestContext(request))
                elif buttonType == 'save and add another':

                # # If buttonType is save and add another show new entry form

                    self.extra_context['prevousId'] = obj.id
                    '''self.extra_context['rank']=self.extra_context.get('rank',0)+1
		    if self.extra_context.get('rank',0)>=self.extra_context.get('rankrange',0):
					self.extra_context['rankrange']=self.extra_context.get('rank')
                    '''
                    if form_class == Question_Form:

                    # If it is a question form pass order

                        self.extra_context['order'] = \
                            Question.objects.filter(assessment__id=self.extra_context['referKey'
                                ]).count() + 1

                    form = \
                        ResourceForm(queryset=queryset.model.objects.none())
                else:
                    if form_class in [Institution_Category_Form,
                            Moi_Type_Form, Institution_Management_Form,
                            Assessment_Form,Assessment_Lookup_Form]:
                        response = \
                            '<input type=hidden id=success_status size=15 value=True /><input type=hidden value=%s id=obj_id />' \
                            % obj.id
                        return response
                    return obj
            else:

            # If form is not valid response back to entry form

                if not DefaultAnswer:

                    if not request.POST.get('defaultanswer', ''):
                        form.errors[0]['defaultanswer'] = \
                            ['The Field is required.']
                    elif request.POST.get('defaultanswer', 'a').lower() \
                        not in ['uk', 'ab']:
                        form.errors[0]['defaultanswer'] = \
                            ['Please enter AB/UK']
                if not AssValid:
                    if not request.POST.get('form-0-primary_field_name'
                            ):
                        form.errors[0]['primary_field_name'] = \
                            ['The Field is required.']
                    if not request.POST.get('form-0-primary_field_type'
                            ):
                        form.errors[0]['primary_field_type'] = \
                            ['The Field is required.']

                '''if not RelationValid:
                    form.errors[0]['motherfirstname'] = 'Any of these fields is required.'
                    print form.errors[0].get('motherfirstname','not')
                '''
                if form_class == Child_Form:
                    self.extra_context['form-0-motherfirstname'] = \
                        request.POST.get('form-0-motherfirstname')
                    self.extra_context['form-0-mothermiddlename'] = \
                        request.POST.get('form-0-mothermiddlename')
                    self.extra_context['form-0-motherlastname'] = \
                        request.POST.get('form-0-motherlastname')
                    self.extra_context['form-0-fatherfirstname'] = \
                        request.POST.get('form-0-fatherfirstname')
                    self.extra_context['form-0-fathermiddlename'] = \
                        request.POST.get('form-0-fathermiddlename')
                    self.extra_context['form-0-fatherlastname'] = \
                        request.POST.get('form-0-fatherlastname')
                    self.extra_context['form-0-otherId'] = \
                        request.POST.get('form-0-otherId')
                self.extra_context['reload']=False
                print 'form ERROR',form.errors
                template_name = '%s/%s_form.html' % (self.template_dir,
                        queryset.model._meta.module_name)
                response = render_to_response(template_name,
                        {'form': form,
                        'extra_context': self.extra_context},
                        context_instance=RequestContext(request))
                return response
        else:

        # If request method is not post get form for the model

            form = ResourceForm(queryset=queryset.model.objects.none())

            # print form
    # Show the form
        self.extra_context['reload']=False
        template_name = '%s/%s_form.html' % (self.template_dir,
                queryset.model._meta.module_name)
        return render_to_response(template_name, {'form': form,
                                  'extra_context': self.extra_context},
                                  context_instance=RequestContext(request))

    def update_form(
        self,
        request,
        pk,
        queryset,
        form_class,
        ):
        """ Render edit form for single entry."""

        elem = queryset.get(**{queryset.model._meta.pk.name: pk})  # get object based on model and pk
        ResourceForm = modelformset_factory(queryset.model,
                form=form_class, extra=0)  # get model formset factory based on model and form
        self.extra_context['showsuccess'] = False  # Pass showsuccess True or false for message
        if request.POST.get('replaceTrue', None) == None:
            self.extra_context['replaceTrue'] = True
        else:
            self.extra_context['replaceTrue'] = False
        print request.POST
        editable = True
        if elem._meta.module_name.lower() == 'assessment':
                obj = Assessment.objects.get(id=pk)

                editable = not obj.getAssessmentStatus()
        print 'EDDDDDDI', editable
        self.extra_context['editable'] = editable

	 
        if request.POST:

        # If request method is post, post data for object
        # form = ResourceForm(request.POST, queryset=queryset.model.objects.filter(pk=pk), )
        # Valid=form.is_valid()  # Validate form
        # print request.POST, Valid

            RelationValid = True
            IValid = True
            new_data = request.POST.copy()
            modelName = queryset.model._meta.module_name

        # Check if current model is child then pass ChildTrue to True else false

            ChildTrue = modelName == 'child' and True or False
            '''
            if ChildTrue:

            # Check for realtion names if names are not there validation fail

                if not (request.POST.get('form-0-fatherfirstname', '')
                        or request.POST.get('form-0-motherfirstname', ''
                        )):
                    RelationValid = False
                    IValid = False
            '''
            print ChildTrue
            AssValid = True
            if form_class == Assessment_Form:
                print 'SSSSSSSSSS'
                if request.POST.get('form-0-flexi_assessment'):
                    print request.POST.get('form-0-flexi_assessment')
                    if not request.POST.get('form-0-primary_field_name'
                            ) \
                        or not request.POST.get('form-0-primary_field_type'
                            ):

                        AssValid = False
            if modelName == 'institution':

            # If Institution Check for address information and if it there update data

                if request.POST.get('form-0-address') \
                    and request.POST.get('form-0-languages') \
                    and request.POST.get('form-0-name'):
                    addressObj = elem.inst_address
                    if addressObj:
                        addressObj.address = \
                            request.POST.get('form-0-address')
                        addressObj.area = request.POST.get('form-0-area'
                                )
                        addressObj.pincode = \
                            request.POST.get('form-0-pincode')
                        addressObj.instidentification = \
                            request.POST.get('form-0-instidentification'
                                )
                        addressObj.landmark = \
                            request.POST.get('form-0-landmark')
                        addressObj.route_information = \
                            request.POST.get('form-0-route_information')
                        addressObj.save()
                    else:
                        addressObj = Institution_address(
                            address=request.POST.get('form-0-address'),
                            area=request.POST.get('form-0-area'),
                            pincode=request.POST.get('form-0-pincode'),
                            instidentification=request.POST.get('form-0-instidentification'
                                    ),
                            landmark=request.POST.get('form-0-landmark'
                                    ),
                            route_information=request.POST.get('form-0-route_information'
                                    ),
                            )
                        addressObj.save()
                    new_data['form-0-inst_address'] = addressObj.id
                    IValid = True

                # Valid = True
                # If request method is post, post data for object

            form = ResourceForm(request.POST,request,
                                queryset=queryset.model.objects.filter(pk=pk))
            Valid = form.is_valid()  # Validate form

            if Valid and IValid and RelationValid and AssValid:
                print 'VAAA',form.errors

            # If From is valid then update data

                obj1 = form.save()
                print obj1
                try:
                    obj = obj1[0]
                except:

                    obj = queryset.model.objects.get(pk=pk)
                print 'OOOOOOOOOOOOOOOOoOBJ',obj
                if modelName == 'child':

                # If model name is child update student data and relations data
                    '''
                    studObj = obj.getStudent()
                    studObj.other_student_id = \
                        request.POST.get('form-0-otherId')
                    studObj.save()
                    
                    relation = {'form-0-motherfirstname': 'Mother',
                                'form-0-fatherfirstname': 'Father'}
                    names = {
                        'Mother-MiddleName': 'form-0-mothermiddlename',
                        'Mother-LastName': 'form-0-motherlastname',
                        'Father-MiddleName': 'form-0-fathermiddlename',
                        'Father-LastName': 'form-0-fatherlastname',
                        }
                    for (rel_type, rel_value) in relation.iteritems():

                        if request.POST[rel_type]:
                            relation = \
                                Relations.objects.filter(relation_type=rel_value,
                                    child=obj)

                            if relation:

                                rel = \
                                    relation.update(first_name=request.POST[rel_type],
                                        middle_name=request.POST[names[rel_value
                                        + '-MiddleName']],
                                        last_name=request.POST[names[rel_value
                                        + '-LastName']])
                            else:

                                relation = \
                                    Relations(relation_type=rel_value,
                                        first_name=request.POST[rel_type],
                                        middle_name=request.POST[names[rel_value
                                        + '-MiddleName']],
                                        last_name=request.POST[names[rel_value
                                        + '-LastName']], child=obj)
                                relation.save()
                        else:

                            relation = \
                                Relations.objects.filter(relation_type=rel_value,
                                    child=obj).delete()
                    '''
                elif modelName == 'staff':

                # If model name is staff update Sg classes

                    mappedClasses = elem.getAssigendClasses()  # get already assigned classes
                    mapClasIds = []
                    classes = \
                        request.POST.getlist('form-0-student_group')  # get newly assigned classes
                    newclasses = [int(i) for i in classes]
                    for mapClas in mappedClasses:
                        mapClasIds.append(mapClas.id)
                        if mapClas.id not in newclasses:

                        # if already assigned class not in newly assigned clasess change relation by changing active state.

                            staff_StudentGroup = \
                                Staff_StudentGroupRelation.objects.filter(staff__id=pk,
                                    student_group=mapClas,
                                    academic=current_academic())[0]
                            staff_StudentGroup.active = 1
                            staff_StudentGroup.save()

                    for clas in newclasses:
                        if clas not in mapClasIds:

                        # if newly assigned class not in already assigned class create relation ship with SG.

                            clasObj = StudentGroup.objects.get(pk=clas)
                            sobj = \
                                Staff_StudentGroupRelation.objects.filter(staff__id=pk,
                                    student_group=clasObj,
                                    academic=current_academic())
                            if sobj:
                                sobj.update(active=2)
                            else:
                                staff_StudentGroup = \
                                    Staff_StudentGroupRelation(staff=elem,
                                        student_group=clasObj,
                                        academic=current_academic(),
                                        active=2)
                                staff_StudentGroup.save()

                buttonType = str(self.extra_context['buttonType'])  # get button type
                self.extra_context['showsuccess'] = True  # make showsuccess is True
                 
                if buttonType == 'save':

                #  If Button type is Save show detail information about updated object

                    respDict = {elem._meta.module_name.lower(): obj,
                                'showsuccess': True}
                    
                    if modelName == 'child':
                        if request.POST['ModelName'] == 'student':
                            respDict['student'] = True

                    if form_class == Staff_Form:
                        template_name = '%s/%s_detail.html' \
                            % ('edittemplates', elem._meta.module_name)
                    else:
                        template_name = '%s/%s_detail.html' \
                            % ('viewtemplates', elem._meta.module_name)
                    response = render_to_response(template_name,
                            respDict,
                            context_instance=RequestContext(request))
                    
                    return response
                elif buttonType == 'save and continue':

                        # If buttonType is save and continue show edit form for the object

                    retFormlist = \
                        ResourceForm(queryset=queryset.model.objects.filter(pk=obj.id))
                elif buttonType == 'save and add another':

                        # # If buttonType is save and add another show new entry form
                    if modelName=='staff':
                         self.extra_context['url']='/institution/'+str(request.POST.get('form-0-institution'))+'/staff/creator/'
                    self.extra_context['prevousId'] = obj.id
                    if form_class == Question_Form:
                        self.extra_context['order'] = \
                            len(Question.objects.filter(assessment__id=self.extra_context['referKey'
                                ])) + 1
                    
                    ResourceForm = modelformset_factory(queryset.model,
                            form=form_class)
                    form = \
                        ResourceForm(queryset=queryset.model.objects.none())
                    template_name = '%s/%s_form.html' % ('viewtemplates'
                            , elem._meta.module_name)
                    response = render_to_response(template_name,
                            {'form': form,
                            'extra_context': self.extra_context},
                            context_instance=RequestContext(request))
                    return response
            else:

                # If form is not valid response back to Edit form

                print RelationValid, 'se'

                # form = ....ResourceForm(request.POST)

                print 'NEXT'
                if not AssValid:
                    if not request.POST.get('form-0-primary_field_name'
                            ):
                        form.errors[0]['primary_field_name'] = \
                            ['The Field is required.']
                    if not request.POST.get('form-0-primary_field_type'
                            ):
                        form.errors[0]['primary_field_type'] = \
                            ['The Field is required.']
                '''if not RelationValid and ChildTrue:

                    form.errors[0]['motherfirstname'] = \
                        ['Any of these fields is required.']
                '''
                if form_class == Child_Form:
                    self.extra_context['form-0-motherfirstname'] = \
                        request.POST.get('form-0-motherfirstname')
                    self.extra_context['form-0-mothermiddlename'] = \
                        request.POST.get('form-0-mothermiddlename')
                    self.extra_context['form-0-motherlastname'] = \
                        request.POST.get('form-0-motherlastname')
                    self.extra_context['form-0-fatherfirstname'] = \
                        request.POST.get('form-0-fatherfirstname')
                    self.extra_context['form-0-fathermiddlename'] = \
                        request.POST.get('form-0-fathermiddlename')
                    self.extra_context['form-0-fatherlastname'] = \
                        request.POST.get('form-0-fatherlastname')
                    self.extra_context['form-0-otherId'] = \
                        request.POST.get('form-0-otherId')
                template_name = '%s/%s_form.html' % (self.template_dir,
                        elem._meta.module_name)
                print template_name,form.errors,'****************'
                return render_to_response(template_name, {
                    'form': form,
                    'update': True,
                    self.template_object_name: elem,
                    'extra_context': self.extra_context,
                    }, context_instance=RequestContext(request))
        else:

        # If request method is not post get form for the model based on pk
            """
            editable = True
            if elem._meta.module_name.lower() == 'assessment':
                obj = Assessment.objects.get(id=pk)

                editable = not obj.getAssessmentStatus()
            print 'EDDDDDDI', editable
            self.extra_context['editable'] = editable
            """
            form = \
                ResourceForm(queryset=queryset.model.objects.filter(pk=pk))

    # Show the form

        template_name = '%s/%s_form.html' % (self.template_dir,
                elem._meta.module_name)
        return render_to_response(template_name, {
            'form': form,
            'update': True,
            self.template_object_name: elem,
            'extra_context': self.extra_context,
            }, context_instance=RequestContext(request))


