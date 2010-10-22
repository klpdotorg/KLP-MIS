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
    url(r'', include('Akshara.AkshararestApi.BoundaryApi')),
    url(r'', include('Akshara.AkshararestApi.SchoolsApi')),
    url(r'', include('Akshara.AkshararestApi.ClassApi')),
    url(r'', include('Akshara.AkshararestApi.ChildApi')),
    url(r'', include('Akshara.AkshararestApi.TreeMenu')),
    url(r'', include('Akshara.AkshararestApi.BoundaryViewApi')),
    url(r'', include('Akshara.AkshararestApi.SchoolViewApi')),
    url(r'', include('Akshara.AkshararestApi.ClassViewApi')),
    url(r'', include('Akshara.AkshararestApi.SectionViewApi')),
    url(r'', include('Akshara.AkshararestApi.StudentViewApi')),

    url(r'', include('Akshara.AkshararestApi.BoundaryTypeApi')),
    url(r'', include('Akshara.AkshararestApi.SchoolCategoryApi')),
    url(r'', include('Akshara.AkshararestApi.LanguageApi')),
    url(r'', include('Akshara.AkshararestApi.ManagementApi')),
    url(r'', include('Akshara.AkshararestApi.ChildEntryApi')),
    url(r'', include('Akshara.AkshararestApi.AcademicEntryApi')),
    url(r'', include('Akshara.AkshararestApi.AutoCompleteApi')),
    url(r'', include('Akshara.AkshararestApi.HomeApi')),
    url(r'', include('Akshara.AkshararestApi.ProgrammeApi')),
    url(r'', include('Akshara.AkshararestApi.AssessmentApi')),
    url(r'', include('Akshara.AkshararestApi.QuestionApi')),
    #url(r'', include('Akshara.AkshararestApi.StudentEvaluationApi')),
    url(r'', include('Akshara.AkshararestApi.AssessmentDetailApi')),
)
