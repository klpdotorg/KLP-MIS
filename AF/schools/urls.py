from django.conf.urls.defaults import *
from schools.views import *

urlpatterns = patterns('',
  (r'^home1/$','schools.views.home1'),
  (r'^home/$','schools.views.home'),
  (r'^search/$','schools.views.search'),

  (r'^boundary-entry/$','schools.views.boundary_entry'),  
  (r'^boundary-schools/$','schools.views.boundary_schools'),  
  (r'^boundary-partition/$', 'schools.views.boundary_partition'),
  (r'^boundary/(?P<boundary_id>\d+)/edit/$','schools.views.boundary_edit'),
  (r'^boundary/(?P<boundary_id>\d+)/view/$','schools.views.boundary_view'),
  (r'^boundary-type/$','schools.views.bound_type'),
  (r'^boundary-list/$','schools.views.boundary_list'),
  (r'^boundary-delete/$','schools.views.boundary_delete'),

  (r'^category-entry/$','schools.views.category_entry'),
  (r'^language-entry/$','schools.views.language_entry'),
  (r'^management-entry/$','schools.views.management_entry'),
  
  (r'^section/(?P<class_id>\d+)/entry/$','schools.views.section_entry'),
  (r'^section/(?P<section_id>\d+)/view/$','schools.views.section_view'),
  (r'^section-delete/$','schools.views.section_delete'),

  (r'^address-entry/$','schools.views.address_entry'),
  (r'^address-edit/(?P<address_id>\d+)/$','schools.views.address_edit'),

  (r'^school/(?P<school_id>\d+)/view/$','schools.views.school_view'),
  (r'^school/(?P<boundary_id>\d+)/entry/$','schools.views.school_entry'),
  (r'^school/(?P<school_id>\d+)/edit/$','schools.views.school_edit'),
  (r'^school-delete/$','schools.views.school_delete'),
  
  (r'^child-entry/$','schools.views.child_entry'),
  (r'^child-edit/(?P<child_id>\d+)/$','schools.views.child_edit'),
  
  (r'^class/(?P<school_id>\d+)/entry/$','schools.views.class_entry'),
  (r'^class/(?P<class_id>\d+)/edit/$','schools.views.class_edit'),
  (r'^class/(?P<class_id>\d+)/view/$','schools.views.class_view'),
  (r'^class-delete/$','schools.views.class_delete'),
  
  (r'^academicyear-entry/$','schools.views.academicyear_entry'),
  (r'^academicyear-edit/(?P<academicyear_id>\d+)/$','schools.views.academicyear_edit'),
  
  (r'^student/(?P<section_id>\d+)/entry/$','schools.views.student_entry'),
  (r'^student/(?P<student_id>\d+)/view/$','schools.views.student_view'),
  (r'^student/(?P<student_id>\d+)/edit/$','schools.views.student_edit'),
  (r'^student-delete/','schools.views.student_delete'),

  
  (r'^get-info/$', 'schools.views.display_info'),
  (r'^get-data/$', 'schools.views.Get_info'),  
  
  
  (r'^tree/(?P<boundary_id>\d+)/structure/$', 'schools.views.treeStructure'),    
)
