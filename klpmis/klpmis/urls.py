from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'klprestApi.AuthenticationApi.KLP_Login'),
    url(r'^home/', 'klprestApi.HomeApi.KLP_Home'),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'static_media'}),

    url(r'', include('klprestApi.HomeApi')),
    url(r'', include('klprestApi.TreeMenu')),
    url(r'', include('klprestApi.BoundaryApi')),
    url(r'', include('klprestApi.InstitutionApi')),
    url(r'', include('klprestApi.InstitutionCategoryApi')),
    url(r'', include('klprestApi.InstitutionManagementApi')),
    url(r'', include('klprestApi.LanguageApi')),
    url(r'', include('klprestApi.ProgrammeApi')),
    url(r'', include('klprestApi.AssessmentApi')),
    url(r'', include('klprestApi.QuestionApi')),
    url(r'', include('klprestApi.StudentGroupApi')),
    url(r'', include('klprestApi.StudentApi')),
    url(r'', include('klprestApi.AuthenticationApi')),
    url(r'', include('klprestApi.AnswerApi')),
    url(r'', include('klprestApi.StaffApi')),
    url(r'', include('klprestApi.ConsoleApi')),
    url(r'', include('klprestApi.KLP_Permission')),
    url(r'', include('klprestApi.KLP_UserApi')),
    url(r'', include('klprestApi.KLP_Map')),
    url(r'', include('klprestApi.KLP_AuditTrial')),
    url(r'', include('klprestApi.AllidsActivate')),
    url(r'', include('klprestApi.KLP_Common')),
)
