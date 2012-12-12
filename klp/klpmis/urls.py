from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'klpmis.views.home', name='home'),
    #url(r'^klpmis/', include('klpmis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below and add
    #'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': 'static_media'}),
    url(r'', include('klpmis.klprestApi.HomeApi')),
    url(r'', include('klpmis.klprestApi.TreeMenu')),
    url(r'', include('klpmis.klprestApi.BoundaryApi')),
    url(r'', include('klpmis.klprestApi.InstitutionApi')),
    url(r'', include('klpmis.klprestApi.InstitutionCategoryApi')),
    url(r'', include('klpmis.klprestApi.InstitutionManagementApi')),
    url(r'', include('klpmis.klprestApi.LanguageApi')),
    url(r'', include('klpmis.klprestApi.ProgrammeApi')),
    url(r'', include('klpmis.klprestApi.AssessmentApi')),
    url(r'', include('klpmis.klprestApi.QuestionApi')),
    url(r'', include('klpmis.klprestApi.StudentGroupApi')),
    url(r'', include('klpmis.klprestApi.StudentApi')),
    url(r'', include('klpmis.klprestApi.AuthenticationApi')),
    url(r'', include('klpmis.klprestApi.AnswerApi')),
    url(r'', include('klpmis.klprestApi.StaffApi')),
    url(r'', include('klpmis.klprestApi.ConsoleApi')),
    url(r'', include('klpmis.klprestApi.KLP_Permission')),
    url(r'', include('klpmis.klprestApi.KLP_UserApi')),
    url(r'', include('klpmis.klprestApi.KLP_Map')),
    url(r'', include('klpmis.klprestApi.KLP_AuditTrial')),
    url(r'', include('klpmis.klprestApi.AllidsActivate')),
    url(r'', include('klpmis.klprestApi.KLP_Common')),
)
