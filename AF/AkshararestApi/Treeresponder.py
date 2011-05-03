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
from django.http import Http404, HttpResponse
from django.forms.util import ErrorDict
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from django.utils import simplejson
from django.utils.xmlutils import SimplerXMLGenerator
from django.views.generic.simple import direct_to_template
import json
from schools.models import StudentGroup,Answer,Student_StudentGroupRelation

class TreeSerializeResponder(object):
    """
    Class for all data formats that are possible
    with Django's serializer framework.
    """
    def __init__(self, CDict,format, mimetype=None, paginate_by=None, allow_empty=False):
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
        self.CDict=CDict
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
        
        response1 = serializers.serialize(self.format, object_list,use_natural_keys=True)
       
        response1= simplejson.loads(response)
        boundary_id = ''
        for k in response1:
		   if k['model'] == "schools.school":
			boundary_id = k['fields']['boundary']
		   imageName=modelName = k['model'].split('.')[-1]
		   if modelName=='studentgroup':
                        imageName=imageName+'_'+k['fields']['group_type']
		   modelName = k['model'].split('.')[-1]
                   childkey= modelName+'_'+str(k['pk'])
                   temval=self.CDict[childkey]
                   childval=temval[0]
                  
                   if childval:
                          childvals='true'  
                          k['hasChildren']=childvals
                   k['id']=childkey
		   names =  k['fields']
                   try:
                        titleval=names['name']
		   except:
			titleval = names['question']
		   k['text'] = temval[1]

	response3 = []
	if boundary_id:
		if self.CDict['filterBy'] != 'None':
			students_list = Answer.objects.filter(question__assessment__programme__id=self.CDict['filterBy'], question__assessment__id=self.CDict['secFilter']).values_list('student',flat=True).distinct('student')
			studentgroup_list = Student_StudentGroupRelation.objects.filter(student__id__in=students_list, active=2,).values_list('student_group', flat=True).distinct()
			object_list1 = StudentGroup.objects.filter(content_type__model="boundary",object_id = boundary_id, active=2,  id__in=studentgroup_list).distinct()
		else:
			object_list1 = StudentGroup.objects.filter(content_type__model="boundary",object_id = boundary_id, active=2,group_type="Center")
		#object_list1 = StudentGroup.objects.filter(content_type__model="boundary",object_id = boundary_id, active=2,group_type="Center")
		response2 = serializers.serialize(self.format, object_list1)
		response3= simplejson.loads(response2)

		for k in response3:
			   imageName=modelName = k['model'].split('.')[-1]
			   if modelName=='studentgroup':
				imageName=imageName+'_'+k['fields']['group_type']
			   childkey= modelName+'_'+str(k['pk'])

			   if self.CDict['filterBy'] != 'None':
				viewlink = '<a href="/studentgroup/'+str(k['pk'])+'/programme/'+str(self.CDict['filterBy'])+'/assessment/'+str(self.CDict['secFilter'])+'/view" onclick="return KLP_View(this)" class="KLP_treetxt" title="">' +k['fields']['name']+'</a>'
			   else:
				viewlink = '<a href="/studentgroup/'+str(k['pk'])+'/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="">' +k['fields']['name']+'</a>'

		           temval=[False,viewlink]
		           childval=temval[0]
		           if childval:
		                  childvals='true'  
		                  k['hasChildren']=childvals
		           k['id']=childkey
			   names =  k['fields']
		           try:
		                titleval=names['name']
			   except:
				titleval = names['question']
			   k['text'] = '<img src="/static_media/tree-images/reicons/'+imageName+'.gif" title='+modelName+' /> &nbsp;'+temval[1]

	response1 = response1+response3

        response=simplejson.dumps(response1)
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
    
class TreeResponder(TreeSerializeResponder):
    """
    JSON data format class.
    """
    def __init__(self,CDict, paginate_by=None, allow_empty=False):
        TreeSerializeResponder.__init__(self,CDict, 'json', 'application/json',
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
