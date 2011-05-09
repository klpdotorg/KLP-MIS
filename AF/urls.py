from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    (r'^akshara/', include('Akshara.schools.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static_media'}),
    url(r'', include('Akshara.AkshararestApi.HomeApi')),
    url(r'', include('Akshara.AkshararestApi.TreeMenu')),
    url(r'', include('Akshara.AkshararestApi.BoundaryApi')),
    url(r'', include('Akshara.AkshararestApi.InstitutionApi')),
    url(r'', include('Akshara.AkshararestApi.InstitutionCategoryApi')),
    url(r'', include('Akshara.AkshararestApi.InstitutionManagementApi')),
    url(r'', include('Akshara.AkshararestApi.LanguageApi')),
    url(r'', include('Akshara.AkshararestApi.ProgrammeApi')),
    url(r'', include('Akshara.AkshararestApi.AssessmentApi')),
    url(r'', include('Akshara.AkshararestApi.QuestionApi')),
    url(r'', include('Akshara.AkshararestApi.StudentGroupApi')),
    url(r'', include('Akshara.AkshararestApi.StudentApi')),
    url(r'', include('Akshara.AkshararestApi.AuthenticationApi')),
    url(r'', include('Akshara.AkshararestApi.AnswerApi')),
    url(r'', include('Akshara.AkshararestApi.StaffApi')),
    url(r'', include('Akshara.AkshararestApi.ConsoleApi')),
    url(r'', include('Akshara.AkshararestApi.KLP_Permission')),
    url(r'', include('Akshara.AkshararestApi.KLP_UserApi')),
    url(r'', include('Akshara.AkshararestApi.KLP_Map')),
    url(r'', include('Akshara.AkshararestApi.KLP_AuditTrial')),
    url(r'', include('Akshara.AkshararestApi.KLP_Common')),
)
