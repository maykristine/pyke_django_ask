pyke_django_ask
===============

"django_ask" module for Python Knowledge Engine (pyke)

documentation
-------------
Spaceman:  OK pyke_test code commited.

me:  got it

Spaceman:  Note that the pyke files need to be compiled by hand at the moment - will automate it in paver at some point.

me:  how?

Spaceman: in settings.py:
PYKE_RULES="directory_name"

in pavement.py:
if settings.PYKE_RULES:
  from pyke import knowledge_engine
Or something like that. :)
