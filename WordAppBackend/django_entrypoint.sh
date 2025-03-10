python manage.py makemigrations --settings=WordAppBackend.settings.prod
python manage.py migrate --settings=WordAppBackend.settings.prod

# 在收集静态文件之前先删除静态文件夹，否则会询问是否覆盖导致报错
rm -rf static
python manage.py collectstatic  --noinput
nohup celery -A WordAppBackend worker -l info > logs/celery.log 2>&1 &
nohup celery -A WordAppBackend beat -l info > logs/celery_bat.log 2>&1 &
# gunicorn --bind=0.0.0.0:8000 --access-logfile=/usr/local/var/log/django/access.log --error-logfile=/usr/local/var/log/django/error.log --capture-output --workers=9 --threads=2 --timeout 30 EmpManagerBackend.wsgi --limit-request-fields 32768 --limit-request-field_size 64000
uwsgi uwsgi.ini
