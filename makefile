## @ Start project
.PHONY: up down
up: ## Starts ALL containers in the project
	docker compose up -d

down: ## Starts ALL containers in the project
	docker compose down

build: ## Starts ALL containers in the project
	docker compose build

logs: ## Starts ALL containers in the project
	docker compose logs

createuser:
	docker container exec -it app python manage.py createsuperuser

migrations:
	docker container exec -it app python manage.py makemigrations

migrate:
	docker container exec -it app python manage.py migrate

autopep8: ## Automatically formats Python code to conform to the PEP 8 style guide
	find -name "*.py" | xargs autopep8 --max-line-length 120 --in-place

isort: ## Organizing the imports
	isort -m 3 *

lint: autopep8 isort

test:
	docker container exec -it app pytest -s