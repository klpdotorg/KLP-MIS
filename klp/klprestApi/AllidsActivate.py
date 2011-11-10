"""

Institution Api is used
1) To view Individual Institution details.
2) To create new Institution
3) To update existing Institution
4) To list boundaries/institutions while assign permissions
"""
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.shortcuts import render_to_response

from schools.models import *
from schools.forms import *



from django.utils import simplejson
from django.template import loader, RequestContext

from django.core.mail import send_mail
from klp.settings import *
from django.views.decorators.csrf import csrf_exempt
#from django.conf import settings

def KLP_act_form(request):
	''' To show the admin form for activate the records '''
	# get logged in user
	user = request.user
	respDict = {'title':'Karnataka Learning Partnership ', 'user':user}
	# render admin console template
	respTemplate = render_to_response("viewtemplates/AllidsActivate_html.html", respDict)
	return HttpResponse(respTemplate)
@csrf_exempt
def KLP_Activation(request):
	""" To actiave the records>"""
	# Checking user Permissions
        #KLP_user_Perm(request.user, "Institution", "Add")
        # Get Button Type
	isExecute=True
	selCategoryTyp = request.POST.get('form-klp-modelname')[0]
	selCategoryids = request.POST.get('form-klp-allids')
	if  selCategoryids=="":
	   isExecute=False
	   resStr="Please give atleast on id"
	   
	   
	else:
	   isExecute=False
	   allids1= selCategoryids.split(',')
           model_name1=  selCategoryTyp=int(selCategoryTyp)
           respDict = {"respStr":selCategoryTyp, "isExecute":isExecute}

           allids=[]
           for k in allids1:
                         allids.append(int(k))    
           modelDict = {1:Boundary, 2:Institution, 4:Programme, 5:Assessment, 6:Question, 3:StudentGroup,  7:Staff, 3:StudentGroup, }
           obj=obj1=modelDict[model_name1].objects.filter(id__in=allids,active=2)
           flag=len(obj1)!=0  
           obj3=modelDict[model_name1].objects.filter(id__in=allids)
           if len(obj3)==0 or len(obj3)!=len(allids):
                  idslist3=obj3.values_list('id')                  
                  idlist4=[]
                  for k in idslist3:
                             idlist4.append(k[0])       
                  resStr=obj1.model._meta.module_name+" Ids "+','.join(str(v) for v in allids if v not in idlist4)+ " are not exist .Please verify the ids ."
  
           elif len(obj1)!=0:
	          idlist1=obj1.values_list('id')
	          resStr=obj1.model._meta.module_name+" Ids "+','.join(str(v1[0]) for v1 in idlist1)+ " are already activated .Please verify the ids." 
	   else:
                obj2=modelDict[model_name1].objects.filter(id__in=allids,active=0)
                isExecute=True   
                idlist2=obj2.values_list('id')
                idstr=','.join(str(v1[0]) for v1 in idlist2)    
                obj2.update(active=2)      
	        
	        SendingMail(idstr,obj2.model._meta.module_name)
	        receiver=settings.REPORTMAIL_RECEIVER
                receiver=','.join(str(v1) for v1 in receiver )
                message="A mail will be sent to %s as soon as all the records are activated ." % (receiver)
	        resStr=obj2.model._meta.module_name+" Ids "+idstr+" are Successfully Activated. "+message		      
	respDict = {"respStr":resStr, "isExecute":isExecute}
	   
        return HttpResponse(simplejson.dumps(respDict), content_type='application/json; charset=utf-8')

def SendingMail(idlist,mname):
                        inst_liststr=idlist
                        sender=settings.REPORTMAIL_SENDER
                        receiver=settings.REPORTMAIL_RECEIVER
                        subject="Activated list"
                        fullmsg="Following %s Ids are Activated  :  \n %s " %(mname,inst_liststr)
                        send_mail(subject, fullmsg, sender,receiver)	
	

urlpatterns = patterns('',    
   url(r'^KLP_activaterecords/$', KLP_Activation),
  url(r'^KLP_activaterecords_form/$', KLP_act_form),
)
