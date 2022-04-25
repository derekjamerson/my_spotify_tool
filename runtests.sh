#! /bin/bash

rm -rf .coverage
coverage run ./manage.py test "$@" -v 2 --noinput &&
coverage report &&
echo "Success"