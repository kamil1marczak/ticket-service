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


REST API Routs:

| URL                                          | HTTP Method | Action               | Permision   | required body key                  |
|----------------------------------------------|-------------|----------------------|-------------|------------------------------------|
| http://localhost:1337/api/event/             | GET         | list of all events   | open to all |                                    |
| http://localhost:1337/api/event/             | POST        | create event         | admin       | event_date_time, name, description |
| http://localhost:1337/api/event/{event_pk}   | GET         | retrieve             | open to all |                                    |
| http://localhost:1337/api/event/{event_pk}   | PUT         | update               | admin       | event_date_time, name, description |
| http://localhost:1337/api/event/{event_pk}   | PATCH       | partial_update       | admin       |                                    |
| http://localhost:1337/api/event/{event_pk}   | DELETE      | destroy              | admin       |                                    |
|                                              |             |                      |             |                                    |
| http://localhost:1337/api/ticket/            | GET         | list of all tickets  | admin       |                                    |
| http://localhost:1337/api/ticket/            | POST        | buy ticket           | open to all | ticket_type, sold_reserved, event  |
| http://localhost:1337/api/ticket/{ticket_id} | GET         | retrieve             | admin       |                                    |
| http://localhost:1337/api/ticket/{ticket_id} | PUT         | update               | admin       |                                    |
| http://localhost:1337/api/ticket/{ticket_id} | PATCH       | buy reserved ticket  | open to all | method ignore body data            |
| http://localhost:1337/api/ticket/{ticket_id} | DELETE      | destroy              | admin       |                                    |
|                                              |             |                      |             |                                    |
| http://localhost:1337/api/account/           | GET         | list of all accounts | admin       |                                    |
| http://localhost:1337/api/account/{currency} | GET         | retrieve             | admin       |                                    |
|                                              |             |                      |             |                                    |
| http://localhost:1337/api/token/             | GET         | receive auth token   | open to all | username, password                 |



TODO:

- test
