from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    (r'^klp/', include('klp.schools.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static_media'}),
    url(r'', include('klp.klprestApi.HomeApi')),
    url(r'', include('klp.klprestApi.TreeMenu')),
    url(r'', include('klp.klprestApi.BoundaryApi')),
    url(r'', include('klp.klprestApi.InstitutionApi')),
    url(r'', include('klp.klprestApi.InstitutionCategoryApi')),
    url(r'', include('klp.klprestApi.InstitutionManagementApi')),
    url(r'', include('klp.klprestApi.LanguageApi')),
    url(r'', include('klp.klprestApi.ProgrammeApi')),
    url(r'', include('klp.klprestApi.AssessmentApi')),
    url(r'', include('klp.klprestApi.QuestionApi')),
    url(r'', include('klp.klprestApi.StudentGroupApi')),
    url(r'', include('klp.klprestApi.StudentApi')),
    url(r'', include('klp.klprestApi.AuthenticationApi')),
    url(r'', include('klp.klprestApi.AnswerApi')),
    url(r'', include('klp.klprestApi.StaffApi')),
    url(r'', include('klp.klprestApi.ConsoleApi')),
    url(r'', include('klp.klprestApi.KLP_Permission')),
    url(r'', include('klp.klprestApi.KLP_UserApi')),
    url(r'', include('klp.klprestApi.KLP_Map')),
    url(r'', include('klp.klprestApi.KLP_AuditTrial')),
    url(r'', include('klp.klprestApi.AllidsActivate')),
    url(r'', include('klp.klprestApi.KLP_Common')),
)
