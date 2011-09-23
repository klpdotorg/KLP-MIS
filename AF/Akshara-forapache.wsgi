import sys
import os

sys.stdout = sys.stderr

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append('/home/akshara');
sys.path.append('/home/akshara/akshara');
sys.path.append('/home/akshara/akshara/Akshara');

import site
site.addsitedir('/home/akshara/akshara/lib/python2.6/site-packages');

os.environ['DJANGO_SETTINGS_MODULE'] = 'Akshara.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

