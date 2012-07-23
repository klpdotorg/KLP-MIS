from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Example:
    (r'^production/', include('production.schools.urls')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'static_media'}),
    url(r'', include('production.klprestApi.HomeApi')),
    url(r'', include('production.klprestApi.TreeMenu')),
    url(r'', include('production.klprestApi.BoundaryApi')),
    url(r'', include('production.klprestApi.InstitutionApi')),
    url(r'', include('production.klprestApi.InstitutionCategoryApi')),
    url(r'', include('production.klprestApi.InstitutionManagementApi')),
    url(r'', include('production.klprestApi.LanguageApi')),
    url(r'', include('production.klprestApi.ProgrammeApi')),
    url(r'', include('production.klprestApi.AssessmentApi')),
    url(r'', include('production.klprestApi.QuestionApi')),
    url(r'', include('production.klprestApi.StudentGroupApi')),
    url(r'', include('production.klprestApi.StudentApi')),
    url(r'', include('production.klprestApi.AuthenticationApi')),
    url(r'', include('production.klprestApi.AnswerApi')),
    url(r'', include('production.klprestApi.StaffApi')),
    url(r'', include('production.klprestApi.ConsoleApi')),
    url(r'', include('production.klprestApi.KLP_Permission')),
    url(r'', include('production.klprestApi.KLP_UserApi')),
    url(r'', include('production.klprestApi.KLP_Map')),
    url(r'', include('production.klprestApi.KLP_AuditTrial')),
    url(r'', include('production.klprestApi.AllidsActivate')),
    url(r'', include('production.klprestApi.KLP_Common')),
)
