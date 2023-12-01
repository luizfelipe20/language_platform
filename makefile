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
	docker compose exec -it app python manage.py createsuperuser

migrations:
	docker compose exec -it app python manage.py makemigrations

migrate:
	docker compose exec -it app python manage.py migrate

phrase_generator:
	docker compose exec -it app python manage.py phrase_generator --tag english_tips_03

remove_duplicate_translations:
	docker compose exec -it app python manage.py remove_duplicate_translations
	
autopep8: ## Automatically formats Python code to conform to the PEP 8 style guide
	find -name "*.py" | xargs autopep8 --max-line-length 120 --in-place

isort: ## Organizing the imports
	isort -m 3 *

lint: autopep8 isort

test:
	docker container exec -it app pytest -s