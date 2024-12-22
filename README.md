# News Store - A Django Rest Framework Project. Simple project to check my skills


## ✏️ **Description of the Project**

This project is built using the Django Rest Framework (DRF) and demonstrates the interaction of the "News Store" with
two primary entities: **users** and **authors**.

---

## 🚀 **Key Features and Tasks**

The project showcases the following:

- Patterns of MVC, MVP. ✅
- Authentication JWT. ✅
- Registration via SMTP protocol.(while deactivated) ✅
- Registration, authorization using Djoser. ✅
- Optimization by connecting phone tasks. ✅
- Optimization using Cache. ✅


---
### 📋 Tasks ###
The project was developed with the aim of exploring the Django Rest Framework.\
Topics such as:
- Patterns of _MVC_, _MVP_. ✅
- Authentication _JWT_. ✅
- Authentication _sessions_. ✅
- Integration. ✅
- Registration via _SMTP_ protocol. ✅
- Registration, authorization using _Djoser_. ✅
- Optimization by connecting _phone tasks_. ✅
- Optimization using _Cache_. ✅

## 📱 Project technologies ##
- Scheme - `Spectacular`.
- Registration - `SMTP`.
- Sending messages - `Djoser`.
- Error tracking - `Sentry (while problems) `.
- Database Backup - `CeleryBeat`.
- Caching and Database - `Redis`.
- Background tasks - `Celery`.




## 📌 **Future Improvements**

- Add payment method(MasterCard e.t.c)
- unit tests
- ssl, nginx configurations 



### 📔 Installing the project in the IDE ###
- Cloning the repository:
```text
git clone https://github.com/GreatTeapot/drf_news.git
```
- Creating a virtual environment and installing dependencies:
```text
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
- Creating `.env` based on `.env.example`
```.env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

PG_DATABASE=
PG_USER=
PG_PASSWORD=
DB_HOST=
DB_PORT=

SENTRY_DSN= (optional)
ACCESS_TOKEN_LIFETIME=
REFRESH_TOKEN_LIFETIME=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=

ALGORITHM=

REDIS_URL=
RABBIT_URL=

CELERY_TASK_TRACK_STARTED=
ACCEPT_CONTENT=
RESULT_SERIALIZER=
TASK_SERIALIZER=
TIMEZONE=

STATIC_FILES=/path/to/static/
MEDIA_FILES=/path/to/media/
```

<a name="installation_docker"></a>
### 🐳 Installing the project in Docker ###
- Build of the project:
```docker
docker-compose up -d --build
```
- Creating migrations:
```docker
docker exec web python manage.py makemigrations
```
- Application of migrations:
```docker
docker exec web python manage.py migrate
```
- Initialization of the project:
```docker
docker-compose exec make initial
```
- Adding a superuser:
```
docker-compose exec web python manage.py createsuperuser
```

<a name="documentation_api"></a>
## 📗 API Documentation ##
API documentation is available at `/api/v1`. \
