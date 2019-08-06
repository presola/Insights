

python3 manage.py makemigrations
python3 manage.py migrate

echo Create first user
DJANGO_DB_NAME=default
DJANGO_SU_NAME=admin
DJANGO_SU_EMAIL=admin@test.com
DJANGO_SU_PASSWORD=testmeagain

python3 -c "import os;os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"HousingInsights.settings\");import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
   username='$DJANGO_SU_NAME', \
   email='$DJANGO_SU_EMAIL', \
   password='$DJANGO_SU_PASSWORD')"

echo "Success"

#gunicorn HousingInsights.wsgi
gunicorn HousingInsights.wsgi:application --workers 4
