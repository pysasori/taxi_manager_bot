#!/bin/sh
#!/usr/bin/env python3

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"