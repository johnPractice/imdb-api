echo "start migrations"
python manage.py makemigrations
echo "start migrate"
python manage.py migrate
echo "run server"
python gunicorn djangoProject1.asgi:application -k uvicorn.workers.UvicornWorker
