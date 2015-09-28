opensrp-plugin
==============

Installation
------------
* Postgres, couchdb should be running

##Git

        git clone https://github.com/DhanushInfotech/opensrp-plugin.git

        cd opensrp-plugin

        virtualenv opensrpweb

        pip install -r requirement.txt

        python manage.py syncdb --noinput

        python manage.py migrate

        python manage.py runserver

==

* run test

        python manage.py test Masters
