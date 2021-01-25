requirement:
Docker, DockerCompose, Redis, Celery, Django

to run app `docker-compose up -d --build`

requirement operation:
1. prepare migration `sudo docker-compose exec web python manage.py makemigrations`
2. execute migration `sudo docker-compose exec web python manage.py migrate`
3. create initial superuser `sudo docker-compose exec web python manage.py createsuperuser`
4. create EUR account in DB`sudo docker-compose exec web python manage.py add_initial_account`
5. populate db with random Event`sudo docker-compose exec web python manage.py add_random_event`

app will be available via http://localhost:1337
admin manager http://localhost:1337/admin

TODO:

- test
- rest API