run:
	python manage.py runserver

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

create_data:
	python manage.py create_data

reset_db:
	python manage.py reset_db --noinput --close-sessions
	python manage.py migrate
	python manage.py createsuperuser \
		--username admin \
		--email admin@example.com \
		--noinput
	python manage.py shell_plus --quiet-load -c "u = User.objects.get(username='admin');u.set_password('12345');u.save();"

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
