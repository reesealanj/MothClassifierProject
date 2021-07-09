#!/bin/bash
coverage erase
coverage run --omit=*/env/* --pylib --include=*/views.py,*/serializers.py,*/permissions.py,*/services.py --branch manage.py test "$@"
coverage report -m