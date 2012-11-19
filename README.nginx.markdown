# An Introduction to KLP 

  The [Karnataka Learning Partnership](http://www.klp.org.in) (KLP) aims to be a partnership of NGOs across 
  Karnataka with these objectives:

  * Create a space where all information pertaining to all children across the state should be made 
    available. This means that it will be our endeavour to work closely with a large number of 
    local NGOs across the state so that they become the channel to collect and update information 
    on a regular basis.
  * Get all children in Karnataka on this database within the next 3-5 years in a phased manner.
  * Give other NGOs the ability to input data pertaining to their programmes as a layer of information
    on the KLP site. For example, Agastya International and Akshaya Patra both serve the same 
    constituency as klp does - if they have access to child databases, then we avoid duplication 
    of efforts and they can use the data for their own interventions and share it on the KLP site.
  * Prepare constituency-wise reports for every elected representative - Members of Parliament, 
    Members of the Legislative Assembly ; Corporators and Panchayat members. This will enable these 
    elected representatives push for an effective agenda for education across the state.
  * Help teachers and head-teachers generate accurate data for DISE reports in a timely manner. 
    This would cover infrastructure of the schools / centres and also the learning outcomes for children.
  * Provide the average citizen adequate information on issues pertaining to education in the state. 
    It is our expectation that those who are on-line and visitors to KLP will find this site informative 
    and that they would be enthused enough to add more data to the site. Over time, we hope that the 
    participation of the community would help in catalyzing and driving demand for quality in education 
    throughout the state.
  * Provide good data to decision makers in government for making effective decisions on investments 
    required for schools across the state. Also, help decision makers at various levels determine where 
    remedial help is required the most and what capacity building needs to be done at different levels.
  * Engage the academic community to use the data and provide analyses that would help in driving policy 
    reforms to provide effective and inclusive education to all children. 


  We believe that if we all work together, it is possible for us to bring in higher levels of quality 
  in our primary education system through a comprehensive use of governance. Nearly 80% of the children 
  in our state use the government primary school system and it is here that, with all our support, 
  we can ensure maximum public good. 

## Vision

  Karnataka Learning Partnership is a public space where all citizens can contribute to the cause of 
  ensuring better schools and schooling for our children . Better education will ensure better human 
  development and prosperity for our citizens. 

# The KLP MIS

  We like to be honest with ourselves as to efficacy and impact of our programmes and the best way 
  that we have found is to collect hard assessment data that we subsequently analyse. This is a 
  challenging task as it requires technology as well as some robust, yet simple processes around the 
  technology.

  Since 2006, the klp Foundation has become increasingly experienced on how best to perform the 
  task laid out above. We are now in a position to design an MIS platform that is sufficiently generic 
  to be used in other organisations in the education sector and perhaps even other sectors. 

## The KLP MIS / EMS components

  * Users
  * Boundaries
  * Institutions
  * Institution Members
  * Institution Owners
  * Programmes
  * Assessments


# Set up of the Development Environment
  In any new environment as SUDO USER, run the following commands<br/>
  `[sudouser@server:~]$ sudo apt-get install python-setuptools python-dev build-essential`<br/>
  `[sudouser@server:~]$ sudo apt-get install libpcre++-dev git gitosis libxml2-dev libssl-dev`<br/>
  `[sudouser@server:~]$ sudo easy_install -U pip`<br/>
  `[sudouser@server:~]$ sudo pip install -U virtualenv`<br/>
  `[sudouser@server:~]$ sudo adduser klpdemo`<br/>
  `[sudouser@server:~]$ su - klpdemo`<br/>

## Database related installation
In any new environment as SUDO USER, run the following commands<br/>
  `[sudouser@server:~]$ apt-get install postgresql-server-dev-8.4 libpq-dev`<br/>

##  Set up a Virtual Python environment
  `[klpdemo@server:~]$ virtualenv --no-site-packages klpsite `<br/>
  `[klpdemo@server:~]$ cd klpsite`<br/>
  `[klpdemo@server:~]$ . bin/activate`<br/>
  Note that the prompt changes after activating to %(klpsite)klpdemo%><br/> 
  Install all required dependencies at this prompt.<br/>
  `[(klpsite)klpdemo@server:~]$ pip install PIL`<br/>
  `[(klpsite)klpdemo@server:~]$ pip install Django==1.2.5`<br/>

## Database related installation
  `[(klpsite)klpdemo@server:~]$ pip install psycopg2`<br/>

##  Set up Django and WSGI
  At the prompt %(klpsite)klpdemo%>, run the following commands while in the ~/klp directory
  If you are a collaborator on this private repository, clone the Git Repo into your home folder on the
  installation box at the prompt %home/miscollabrator%>.<br/>
  `[miscollaborator@server:~]$ git clone git://github.com/klpdotorg/KLP-MIS.git`<br/>
  Now copy the checkout folder at the prompt  %(klpsite)klpdemo%/home/klp> <br/>
  `[(klpsite)klpdemo@server:~]$ cp -r /home/miscollaborator/KLP-MIS/klp ~/klpsite/`<br/>
  `[(klpsite)klpdemo@server:~]$ cd ~/klpsite/klp`<br/>
  `[(klpsite)klpdemo@server:~]$ vi klp.wsgi`<br/>
  The content of this file should be:<br/>
  > import sys<br/>
  > sys.stdout = sys.\_\_stdout\_\_<br/>
  > sys.stderr = sys.\_\_stderr\_\_<br/>
  > sys.path.append('/home/klpdemo/klpsite/klp/lib/python2.6/site-packages')<br/>
  > sys.path.append('/home/klpdemo/klpsite/klp/lib/python2.6/lib-dynload')<br/>
  > sys.path.append('/home/klpdemo/klpsite/klp/lib/python2.6')<br/>
  > sys.path.append('/home/klpdemo/klp')<br/>
  > import os<br/>
  > os.environ['DJANGO_SETTINGS_MODULE'] = 'klp.settings'<br/>
  > import django.core.handlers.wsgi<br/>
  > application = django.core.handlers.wsgi.WSGIHandler()<br/>

## Configuration in settings.py
  The content of settings.py file in should carry Postgres DB details:<br/>
  `[(klpsite)klpdemo@server:~]$ cd ~/klp/`<br/>
  `[(klpsite)klpdemo@server:~]$ vi settings.py`<br/>
  > DATABASES = {<br/>
  >  'default': {<br/>
  >      'ENGINE': 'postgresql_psycopg2'<br/>
  >      'USER': '',<br/>
  >      'PASSWORD': '',<br/>
  >      'HOST': '',<br/>
  >      'PORT': '',<br/>
  >  }<br/>
  >}<br/>
  Additionally make sure the directory path to the Django installation is correctly indicated, for eg in the line: <br/>
  > TEMPLATE_DIRS = (<br/>
  >  '/home/klpdemo/klpsite/klp/schools/templates/',<br/>
  >)<br/>


##  Set up Nginx and uWSGI
  `[(klpsite)klpdemo@server:~]$ mkdir programs`<br/>
  `[(klpsite)klpdemo@server:~]$ cd programs`<br/>
  `[(klpsite)klpdemo@server:~]$ wget http://nginx.org/download/nginx-0.8.53.tar.gz`<br/>
  `[(klpsite)klpdemo@server:~]$ wget http://nginx-init-ubuntu.googlecode.com/files/nginx-init-ubuntu_v2.0.0-RC2.tar.bz2`<br/>
  `[(klpsite)klpdemo@server:~]$ wget http://projects.unbit.it/downloads/uwsgi-0.9.6.5.tar.gz`<br/>
  `[(klpsite)klpdemo@server:~]$ tar xvf nginx-0.8.53.tar.gz`<br/>
  `[(klpsite)klpdemo@server:~]$ tar xvf uwsgi-0.9.6.5.tar.gz`<br/>
  `[(klpsite)klpdemo@server:~]$ mkdir ~/nginx`<br/>
  `[(klpsite)klpdemo@server:~]$ cd nginx-0.8.53`<br/>
  `[(klpsite)klpdemo@server:~]$ ./configure --without-http_uwsgi_module --add-module=../uwsgi-0.9.6.5/nginx/ --prefix=/home/klpdemo/nginx`<br/>

Disable unbuilt uWSGI(thats old) and includes latest uwsgi package<br/>
  `[(klpsite)klpdemo@server:~]$ make`<br/>
  `[(klpsite)klpdemo@server:~]$ make install`<br/>
  `[(klpsite)klpdemo@server:~]$ cd ../uwsgi-0.9.6.5`<br/>
  `[(klpsite)klpdemo@server:~]$ make -f Makefile`<br/>
  `[(klpsite)klpdemo@server:~]$ cp uwsgi ~/klp/bin/`<br/>
  `[(klpsite)klpdemo@server:~]$ cp uwsgi_params ~/nginx/`<br/>
  `[(klpsite)klpdemo@server:~]$ cd ~/nginx`<br/>
  `[(klpsite)klpdemo@server:~]$ mkdir vhost`<br/>
  `[(klpsite)klpdemo@server:~]$ vi ~/nginx/conf/nginx.conf`<br/>

The content of this file should include vhost in the http context and
make sure you comment out default 'location /' context in here <br/>
  > include vhost/*.conf;<br/>

Also change the content of the django.conf
  `[(klpsite)klpdemo@server:~] vi nginx/vhost/django.conf`<br/>
Add the django virtualhost config (Assuming 192.168.2.2 is the system ip)<br/>
  > upstream django {<br/>
  > ip_hash;<br/>
  > server 192.168.2.2:8010;<br/>
  > comment out:#server unix:sock/uwsgi.sock;<br/>
  > }<br/>
  > server {<br/>
  > listen 80;<br/>
  > server_name  klp.mahiti.org;<br/>
  > location /static_media/ {<br/>
  >   alias /home/klpdemo/klpsite/klp/static_media/;<br/>
  > }<br/>
  > location / {<br/>
  > uwsgi_pass  django;<br/>
  > comment out:#uwsgi_param UWSGI_SCRIPT mcms.pac;<br/>
  > include   uwsgi_params;<br/>
  > }<br/>
  > }<br/>

  `[(klpsite)klpdemo@server:~]$ cd ~/klpsite/klp`<br/>
  `[(klpsite)klpdemo@server:~]$ uwsgi -s 192.168.2.2:8010 -M --wsgi-file klp.wsgi`<br/>
Check if uwsgi runs without errors. Ctrl-C to exit.<br/>

##  Setup Supervisor
As ROOT user set up Supervisor:<br/>
  `[root@server:~]$ pip install supervisor`<br/>
  `[root@server:~]$ echo_supervisord_conf > ~/etc/supervisord.conf`<br/>
  `[root@server:~]$ vi ~/etc/supervisord.conf`<br/>

Change supervisor sock and logs path to /home/klpdemo/klpsite/klp/logs<br/>
And add control for uwsgi <br/>
  > [group:klp-ems]<br/>
  > programs=uwsgi,nginx<br/>
  > [program:uwsgi]<br/>
  > command=/home/klpdemo/klpsite/klp/bin/uwsgi --socket 192.168.2.2:8010 --processes 5 --master --wsgi-file klp.wsgi<br/>
  > directory=/home/klpdemo/klpsite/klp/<br/>
  > user=klpdemo<br/>
  > autostart=true<br/>
  > autorestart=true<br/>
  > stdout_logfile=/home/klpdemo/klpsite/klp/logs/uwsgi.log<br/>
  > redirect_stderr=true<br/>
  > stopsignal=QUIT<br/>
  > [program:nginx]<br/>
  > command=/home/klpdemo/nginx/sbin/nginx -c /home/klpdemo/nginx/conf/nginx.conf -g "daemon off;"<br/>
  > directory=/home/klpdemo/<br/>
  > user= root<br/>
  > autostart=true<br/>
  > autorestart=true<br/>
  > stopsignal=QUIT<br/>

Download the init-script for supervisor to /etc/init.d/<br/>
  `[root@server:~]$ cd /etc/init.d`<br/>
  `[root@server:~]$ wget -O supervisord http://svn.supervisord.org/initscripts/debian-norrgard`<br/>
  `root@server:~]$ chmod +x supervisord`<br/>

small changes in the script<br/>
check where the supervisord binary(command program) is installed<br/>
  `[root@server:~]$ which supervisord`<br/>
In some cases maybe /usr/local/bin/supervisord or /usr/bin or /usr/sbin<br/>
  `[root@server:~]$ vi /etc/init.d/supervisord`<br/>
Put the right path for supervisor in line 25 of the script.<br/>
Repeat this to correct the path of supervisorctl too.<br/>
Specify the full path at line 75 for supervisorctl.<br/>
Add a group for controlling ems:<br/>
  `[root@server:~]$ groupadd emsadmin`<br/>
  `[root@server:~]$ usermod -a -G emsadmin klpdemo`<br/>
  `[root@server:~]$ chgrp emsadmin /etc/supervisord.conf`<br/>
  `[root@server:~]$ chmod 660 /etc/supervisord.conf`<br/>
  `[root@server:~]$ vi /etc/supervisord.conf`<br/>

Make sure the sock permssion is changed in the config as<br/>
  > [unix_http_server]<br/>
  > file=/tmp/supervisor.sock<br/>
  > chmod=0760<br/>  
  > chown=root:emsadmin<br/>

Check if supervisor functions fine:<br/>
  `[root@server:~]$ /etc/init.d/supervisord restart`<br/>
  `[root@server:~]$ su - klpdemo`<br/>

  `[klpdemo@server:~]$ supervisorctl start klp-ems:uwsgi`<br/>
  `[klpdemo@server:~]$ supervisorctl start klp-ems:nginx`<br/>
  `[klpdemo@server:~]$ supervisorctl status`<br/>
Check for:<br/>
klp-ems:nginx                    RUNNING    pid 26046, uptime 0:13:19<br/>
klp-ems:uwsgi                    RUNNING    pid 26036, uptime 0:13:52<br/>

## Bringing up the Application
Now you should be having a django app rendered at http://<server_ip>:80/home/<br/>

