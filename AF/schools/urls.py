from django.conf.urls.defaults import *
from Akshara.schools.views import *

urlpatterns = patterns('',
  (r'^home1/$','Akshara.schools.views.home1'),
  (r'^home/$','Akshara.schools.views.home'),
  (r'^search/$','Akshara.schools.views.search'),

  (r'^boundary-entry/$','Akshara.schools.views.boundary_entry'),  
  (r'^boundary-schools/$','Akshara.schools.views.boundary_schools'),  
  (r'^boundary-partition/$', 'Akshara.schools.views.boundary_partition'),
  (r'^boundary/(?P<boundary_id>\d+)/edit/$','Akshara.schools.views.boundary_edit'),
  (r'^boundary/(?P<boundary_id>\d+)/view/$','Akshara.schools.views.boundary_view'),
  (r'^boundary-type/$','Akshara.schools.views.bound_type'),
  (r'^boundary-list/$','Akshara.schools.views.boundary_list'),
  (r'^boundary-delete/$','Akshara.schools.views.boundary_delete'),

  (r'^category-entry/$','Akshara.schools.views.category_entry'),
  (r'^language-entry/$','Akshara.schools.views.language_entry'),
  (r'^management-entry/$','Akshara.schools.views.management_entry'),
  
  (r'^section/(?P<class_id>\d+)/entry/$','Akshara.schools.views.section_entry'),
  (r'^section/(?P<section_id>\d+)/view/$','Akshara.schools.views.section_view'),
  (r'^section-delete/$','Akshara.schools.views.section_delete'),

  (r'^address-entry/$','Akshara.schools.views.address_entry'),
  (r'^address-edit/(?P<address_id>\d+)/$','Akshara.schools.views.address_edit'),

  (r'^school/(?P<school_id>\d+)/view/$','Akshara.schools.views.school_view'),
  (r'^school/(?P<boundary_id>\d+)/entry/$','Akshara.schools.views.school_entry'),
  (r'^school/(?P<school_id>\d+)/edit/$','Akshara.schools.views.school_edit'),
  (r'^school-delete/$','Akshara.schools.views.school_delete'),
  
  (r'^child-entry/$','Akshara.schools.views.child_entry'),
  (r'^child-edit/(?P<child_id>\d+)/$','Akshara.schools.views.child_edit'),
  
  (r'^class/(?P<school_id>\d+)/entry/$','Akshara.schools.views.class_entry'),
  (r'^class/(?P<class_id>\d+)/edit/$','Akshara.schools.views.class_edit'),
  (r'^class/(?P<class_id>\d+)/view/$','Akshara.schools.views.class_view'),
  (r'^class-delete/$','Akshara.schools.views.class_delete'),
  
  (r'^academicyear-entry/$','Akshara.schools.views.academicyear_entry'),
  (r'^academicyear-edit/(?P<academicyear_id>\d+)/$','Akshara.schools.views.academicyear_edit'),
  
  (r'^student/(?P<section_id>\d+)/entry/$','Akshara.schools.views.student_entry'),
  (r'^student/(?P<student_id>\d+)/view/$','Akshara.schools.views.student_view'),
  (r'^student/(?P<student_id>\d+)/edit/$','Akshara.schools.views.student_edit'),
  (r'^student-delete/','Akshara.schools.views.student_delete'),

  
  (r'^get-info/$', 'Akshara.schools.views.display_info'),
  (r'^get-data/$', 'Akshara.schools.views.Get_info'),  
  
  
  (r'^tree/(?P<boundary_id>\d+)/structure/$', 'Akshara.schools.views.treeStructure'),    
)
