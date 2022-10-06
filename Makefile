.ONESHELL:

python := $(py) python

define setup_env
    $(eval ENV_FILE := $(1))
    @echo " - setup env $(ENV_FILE)"
    $(eval include $(1))
    $(eval export)
endef

.PHONY: release
release:
	docker compose up --build

.PHONY: release-up
release-up:
	docker compose up

.PHONY: release-build
release-build:
	docker compose build

.PHONY: dev
dev:
	docker compose -f=docker-compose-dev.yaml up --build

.PHONY: dev-up
dev-up:
	docker compose -f=docker-compose-dev.yaml up

.PHONY: dev-build
dev-build:
	docker compose -f=docker-compose-dev.yaml build

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
