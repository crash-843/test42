MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) test core
collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) collectstatic --noinput
run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) runserver
syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) syncdb --noinput --no-initial-data
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) migrate
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) syncdb --noinput