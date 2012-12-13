from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'klpmis.views.home', name='home'),
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
