# opensrp-admin
This is a standalone admin module to create and update Masters

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

        python manage.py syncdb --noinput

        python manage.py migrate

        python manage.py runserver

==

* run test

        python manage.py test Masters