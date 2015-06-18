# earkweb
E-ARK integrated prototype web application

## Developer notes

### Checkout project

    git clone https://github.com/eark-project/earkweb

### Virtual environment (python)

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    mkvirtualenv <name>
    workon <name>

### Install additional libraries

    sudo pip install Django==1.7
    sudo pip install requests
    sudo pip install lxml

### Local development

Change path so that it detects your local development path in earkweb/earkweb/urls.py:

    if "Development/" ...

Set the file to "assume-unchanged":

    git update-index --assume-unchanged earkweb/earkweb/urls.py

and undo if needed:

    git update-index --no-assume-unchanged earkweb/earkweb/urls.py

### Enable CAS in Django

Requires CAS server (see below):

Requires mercurial:

    sudo apt-get install mercurial

Get module from https://bitbucket.org/cpcc/django-cas

    hg clone https://bitbucket.org/cpcc/django-cas
    
## Install CAS server

### Prepare Apache Tomcat (enable SSL)

1. Create keystore

    keytool -genkey -alias tomcat -keyalg RSA -keystore keystore.jks

2. Activate SSL using the keystore (in conf/server.xml):

    <Connector port="8443" 
        keystoreFile="/usr/local/java/apache-tomcat-7.0.56/keystore.jks" 
        keystorePass="changeit" 
        protocol="org.apache.coyote.http11.Http11NioProtocol"
        maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
        clientAuth="false" sslProtocol="TLS" />


    cp cas-server-4.0.0/modules/cas-server-webapp-4.0.0.war $TOMCAT_HOME/webapps/

### Deploy CAS

1. Download CAS

    http://downloads.jasig.org/cas/cas-server-4.0.0-release.tar.gz

2. Deploy CAS WAR to Apache Tomcat

    cp cas-server-4.0.0/modules/cas-server-webapp-4.0.0.war $TOMCAT_HOME/webapps/

3. Install

    cd django-cas
    sudo python setup.py install


