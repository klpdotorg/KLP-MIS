from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'klprestApi.AuthenticationApi.klp_login'),
    url(r'^admin/', include(admin.site.urls)),
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

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
