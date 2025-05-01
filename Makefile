#!make

.PHONY: help env manage requirements

.DEFAULT_GOAL := help

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


# Function to export environment variables from a file
define export_env
	@echo "--- Exporting: $(1)"
	$(eval include $(1))
    $(eval export)
endef


##@ Development Environment
env: ## Export environment variables from .env - Generate from .env.default if not found
	@if [ ! -f .env ]; then \
		cp .env.default .env; \
		echo "--- Generated .env from .env.default"; \
	fi
	$(call export_env, .env.default)
	$(call export_env, .env)

install_uv: ## Install uv if not found
	@if ! uv -V ; then \
        echo "uv not found, installing..."; \
        curl -LsSf https://astral.sh/uv/install.sh | sh; \
		source $(HOME)/.cargo/env ; \
    else \
        echo "uv is already installed. Skipped."; \
    fi

venv: install_uv env ## Initialize a new virtual environment in UV_PROJECT_ENVIRONMENT
	uv venv --seed

activate-venv: env ## Activate the virtual environment
	. $(UV_PROJECT_ENVIRONMENT)/bin/activate && exec $$SHELL

requirements: env ## Install all dependencies including dev, extras
	uv sync

# Execute uv with the variable UV_PROJECT_ENVIRONMENT defined in .env
# Example: > make uv tree -- --outdated
uv: env ## Execute uv commands with the custom environment
	uv $(filter-out $@, $(MAKECMDGOALS))


##@ Code Quality
lint: env ## Run the linters
	uv run ruff format --check .
	uv run ruff check .

lint-fix: env ## Apply linting and formatting fixes to codebase - use with caution
	uv run ruff format .
	uv run ruff check --fix .

type-check: env ## Run the static type checker
	uv run mypy .

lint-ci: lint type-check ## Run the linters and static type checker for CI

##@ Testing
test: env ## Run the tests in local environment
	uv run pytest .

test-lock: env ## Verify that uv.lock is up-to-date
	uv lock --check

test-ci: test-lock test ## Specific test command for GitHub CI environment

check-all: lint-ci test ## Run all checks and tests


##@ Docker Management
DOCKER_COMMAND = @docker compose -f docker-compose.yml

down: ## Stop all services
	$(DOCKER_COMMAND) down

up: env down ## Build and run selected services
	@echo "Launching docker services: $(DOCKER_SERVICES)"
	$(DOCKER_COMMAND) up -d --build $(DOCKER_SERVICES)


##@ Django commands
DJANGO_MANAGE = uv run manage.py

migrations: env ## Generate Django migrations
	$(DJANGO_MANAGE) makemigrations

migrations-check: env ## Verify latest Django migrations
	$(DJANGO_MANAGE) makemigrations --noinput --check

migrate: env ## Apply Django migrations
	$(DJANGO_MANAGE) migrate $(filter-out $@, $(MAKECMDGOALS))

run: env ## Run the Django development server
	$(DJANGO_MANAGE) runserver 0.0.0.0:$(API_PORT)

# For commands with optional arguments (--), add an additional -- beforehand:
# > make manage startapp newapp
# > make -- manage createsuperuser --username admin --email admin@admin.fr
manage: env ## Execute Django management commands
	$(DJANGO_MANAGE) $(filter-out $@, $(MAKECMDGOALS))

%:
	@true
