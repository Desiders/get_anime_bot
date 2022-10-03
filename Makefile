.ONESHELL:

python := $(py) python

define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: release-up
release-up:
	docker compose -f=docker-compose.yaml --env-file=.env up

.PHONY: release-build
release-build:
	docker compose -f=docker-compose.yaml --env-file=.env build

.PHONY: release
release:
	docker compose -f=docker-compose.yaml --env-file=.env up --build

.PHONY: dev-up
dev-up:
	docker compose -f=docker-compose-dev.yaml --env-file=.env.dev up

.PHONY: dev-build
dev-build:
	docker compose -f=docker-compose-dev.yaml --env-file=.env.dev build

.PHONY: dev
dev:
	docker compose -f=docker-compose-dev.yaml --env-file=.env.dev up --build

.PHONY: migration-head
migration-head:
	$(call setup_env, .env)
	alembic upgrade head

.PHONY: migration-head-dev
migration-head-dev:
	$(call setup_env, .env.dev)
	alembic upgrade head

.PHONY: migration-up
migration-up:
	$(call setup_env, .env)
	alembic upgrade +1

.PHONY: migration-up-dev
migration-up-dev:
	$(call setup_env, .env.dev)
	alembic upgrade +1

.PHONY: migration-down
migration-down:
	$(call setup_env, .env)
	alembic downgrade -1

.PHONY: migration-down-dev
migration-down-dev:
	$(call setup_env, .env.dev)
	alembic downgrade -1

.PHONY: generate-first-migration
generate-first-migration:
	$(call setup_env, .env)
	alembic revision --autogenerate -m "Create tables"

.PHONY: generate-first-migration-dev
generate-first-migration-dev:
	$(call setup_env, .env.dev)
	alembic revision --autogenerate -m "Create tables"
