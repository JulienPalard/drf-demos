# Fixtures

Can be loaded using:

    ./manage.py loaddata initial

Can be saved back using:

    ./manage.py dumpdata -e contenttypes -e auth.Permission -e sessions.session -o uptime/fixtures/initial.json

Initial data contains 3 users:

- admin:admin, owning mdk.fr
- alice:alice, owning afpy.org
- bob:bob owning bbb.afpy.org

(Notice **a**lice own **a**fpy.org and **b**ob owns **b**bb.afpy.org.)


## TODO

- [x] flake8 flake8-bugbear
- [x] pylint pylint-django
- [x] mypy
- [x] black
- [x] isort
- [x] pydocstyle
- [x] bandit
- [x] tox
