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
    constituency as Akshara does - if they have access to child databases, then we avoid duplication 
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

  Since 2006, the Akshara Foundation has become increasingly experienced on how best to perform the 
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


# Set up the Development Environment
  In any new environment as SUDO USER, run the following commands<br/>
  `[sudouser@server:~]$ sudo apt-get install python-setuptools python-dev build-essential checkinstall`<br/>
  `[sudouser@server:~]$ sudo apt-get install libpcre++-dev git gitosis libxml2-dev libssl-dev`<br/>
  `[sudouser@server:~]$ sudo easy_install -U pip`<br/>
  `[sudouser@server:~]$ sudo adduser aksharademo`<br/>

## Database related installation
In any new environment as SUDO USER, run the following commands<br/>
  `[sudouser@server:~]$ sudo apt-get install postgresql-server-dev-8.4 libpq-dev`<br/>
  `[sudouser@server:~]$ sudo pip install psycopg2`<br/>

##  Set up Python environment
  `[sudouser@server:~]$ sudo pip install PIL`<br/>
  `[sudouser@server:~]$ sudo pip install Django==1.2.5`<br/>

##  Set up Apache and mod-wsgi
  Install Apache Worker MPM, which is recommended as it processes requests using threads.(Will produce results faster)<br/>
  `[sudouser@server:~]$ sudo apt-get install apache2 apache2-mpm-worker apache2-threaded-dev`<br/>
  Download the latest stable tar files of mod-wsgi from http://code.google.com/p/modwsgi/downloads/ <br/>
  Extract the tar file and cd into the directory.<br/>
  Compile and install<br/>
  `[sudouser@server:~ mod-wsgi-ver]$ ./configure`<br/>
  `[sudouser@server:~ mod-wsgi-ver]$ make`<br/>
  `[sudouser@server:~ mod-wsgi-ver]$ sudo checkinstall`
  Follow the prompts in checkinstall.<br/>
  By default, there is no need to change anything here. You can just keep typing 'Enter'.<br/>
  After the install is finished successfully, Restart Apache server once.<br/>
  `[sudouser@server:~]$ sudo service apache2 restart`<br/>

##  Set up Django and WSGI
  At the prompt %aksharademo% >, run the following commands while in the ~/akshara directory
  If you are a collaborator on this private repository, clone the Git Repo into your home folder on the
  installation box at the prompt %home/miscollabrator% >.<br/>
  `[miscollaborator@server:~]$ git clone git@github.com:gkjohn/Akshara-MIS.git`<br/>
  Now copy the checkout folder at the prompt  %aksharademo% /home/akshara> <br/>
  `[sudouser@server:~]$ su - aksharademo`<br/>
  `[aksharademo@server:~]$ cp -r /home/miscollaborator/Akshara/Akshara-MIS/AF Akshara`<br/>
  `[aksharademo@server:~]$ cd ~/akshara/Akshara`<br/>
  `[aksharademo@server:~]$ vi Akshara.wsgi`<br/>
  The content of this file should be:<br/>
  > import sys<br/>
  > sys.stdout = sys.\_\_stdout\_\_<br/>
  > sys.stderr = sys.\_\_stderr\_\_<br/>
  > sys.path.append('/home/aksharademo/akshara')<br/>
  > import os<br/>
  > os.environ['DJANGO_SETTINGS_MODULE'] = 'Akshara.settings'<br/>
  > import django.core.handlers.wsgi<br/>
  > application = django.core.handlers.wsgi.WSGIHandler()<br/>

## Configuration in settings.py
  The content of settings.py file in should carry Postgres DB details:<br/>
  `[aksharademo@server:~]$ cd ~/akshara/Akshara`<br/>
  `[aksharademo@server:~]$ vi settings.py`<br/>
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
  >  '/home/aksharademo/akshara/Akshara/schools/templates/',<br/>
  >)<br/>


## Bringing up the Application
Now you should be having a django app rendered at http://\<server_ip\>/<br/>

