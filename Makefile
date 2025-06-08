run:
	python manage.py runserver & celery -A root worker --loglevel=info


mig:
	python manage.py makemigrations
	python manage.py migrate