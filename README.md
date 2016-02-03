<a href="https://travis-ci.org/DhanushInfotech/opensrp-plugin">
<img src="https://travis-ci.org/DhanushInfotech/opensrp-plugin.svg?branch=master" ></img></a>

<a href='https://coveralls.io/github/DhanushInfotech/opensrp-plugin?branch=django-module'><img src='https://coveralls.io/repos/DhanushInfotech/opensrp-plugin/badge.svg?branch=django-module&service=github' alt='Coverage Status' /></a> 

# opensrp-plugin
This is a standalone admin module to create and update Master data

1. Manage user accounts

2. Maintain Doctors and Plan of Care Data

3. Manage Drugs and relevant info

NOTE: This is a standalone module within Opensrp application developed using Django Framework and yet to be improved further

# opensrp-plugin


Installation
------------
* Postgres, couchdb should be running

##Git

        git clone https://github.com/DhanushInfotech/opensrp-plugin.git

        cd opensrp-plugin

        virtualenv opensrpweb

        sudo apt-get update

        sudo apt-get install libpq-dev python-dev

        pip install -r requirement.txt

        pip install coverage
        
        python manage.py syncdb --noinput

        python manage.py migrate

        python manage.py runserver

==

* run test

        coverage run --source='.' manage.py test
        coverage report -m
