from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django_restapi.resource import Resource
from schools.models import *
from schools.forms import *
from django_restapi.model_resource import Collection, Entry
from django_restapi.responder import *
from django_restapi.receiver import *
from AkshararestApi.BoundaryApi import ChoiceEntry
from django.template import RequestContext
#from pysqlite2 import dbapi2 as sqlite
import psycopg2
from django.utils import simplejson

def KLP_Admin_Console(request):
	''' To show the admin Console to run SQl Queries '''
	user = request.user
	respDict = {'title':'Karnataka Learning Partnership ', 'user':user}
	respTemplate = render_to_response("viewtemplates/admin_console.html", respDict)
	return HttpResponse(respTemplate)
      
def KLP_Run_Query(request):  
    ''' To run SQl Queries Entered by admin''' 
    adminQuery = request.POST.get('form-klp-query')
    #connection = sqlite.connect('/home/akshara/Akshara/akshara.db')
    connection = psycopg2.connect(database="newklp", user="aksharadb", password="RObu15tFTG")
    cursor = connection.cursor()
    isExecute = False
    if adminQuery:
	    try:
	    	cursor.execute(adminQuery)
	    	respStr = "Query Executed Sucessfully"
	    	isExecute = True
	    except:
	    	respStr = "Query You Written May Incorrect, Please Check It"
    else:	
    	respStr = "Query You Send Is Empty"
    cursor.close()
    respDict = {"respStr":respStr, "isExecute":isExecute}
    return HttpResponse(simplejson.dumps(respDict), content_type='application/json; charset=utf-8')
      

urlpatterns = patterns('',             
   url(r'^console/?$', KLP_Admin_Console), 
   url(r'^run-query/?$', KLP_Run_Query),   
)
