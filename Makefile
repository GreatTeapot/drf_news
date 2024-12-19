
# ------------------------------------- INIT ----------------------------------------

.PHONY: init
init:
# Set up a virtual environment.
	python -m venv venv
# Activate the virtual environment.
	source venv/bin/activate
# Install project dependencies.
	pip install -r requirements.txt
# -----------------------------------------------------------------------------------

# ----------------------------- MIGRATIONS AND STATIC -------------------------------
# Apply migrations and execute them.
.PHONY: migrations
migrations:
	python ./manage.py makemigrations
	python ./manage.py migrate

# Collect static files.
.PHONY: static
static:
	python ./manage.py collectstatic
# -----------------------------------------------------------------------------------

# ----------------------------------- LOAD DATA -------------------------------------
# Load data into the database.
.PHONY: load
load:
	python ./manage.py loaddata fixtures/categories.json
	python ./manage.py loaddata fixtures/providers.json
	python ./manage.py loaddata fixtures/products.json
	python ./manage.py loaddata fixtures/products_description.json
	python ./manage.py loaddata fixtures/products_feature.json
	python ./manage.py loaddata fixtures/products_images.json
# -----------------------------------------------------------------------------------

# ------------------------------------- SUPERUSER -----------------------------------
# Create a superuser.
.PHONY: createsuperuser
createsuperuser:
	python ./manage.py createsuperuser
# -----------------------------------------------------------------------------------

# ------------------------------ RUN AND STOP SERVER --------------------------------
# Start the development server.
.PHONY: run
run:
	python manage.py runserver

# Stop the development server.
.PHONY: stop
stop:
	pkill -f "python ./manage.py runserver"
# -----------------------------------------------------------------------------------

# ------------------------------------- CELERY --------------------------------------
# Start Celery. Maksde sure you have Redis running (on WSL2 if you're on Windows)
# and RabbitMQ is running on your local host!
.PHONY: celery
celery:
	celery --app=config worker --loglevel=info --pool=solo

# Start Celery Beat for database backups.
.PHONY: beat
beat:
	celery -A config beat -l info
