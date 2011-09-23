import sys

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

sys.path.append('/home/akshara/akshara/lib/python2.6/site-packages')
sys.path.append('/home/akshara/akshara/lib/python2.6')
sys.path.append('/home/akshara/akshara')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Akshara.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
