VERSION = `git rev-parse --short HEAD`
TO := _
SKIP_SLEEP ?= 0

COMPOSE = docker-compose -p debezium_supervisor

.PHONY: init
init:
	# This following command is used to provision the network
	$(COMPOSE) up --no-start --no-build app | true

.PHONY: run
run:
	$(COMPOSE) build app
	$(COMPOSE) up app



.PHONY: down
down:
	$(COMPOSE) down --volumes


.PHONY: format
format:
	$(COMPOSE) build format-imports
	$(COMPOSE) run format-imports
	$(COMPOSE) build format
	$(COMPOSE) run format


.PHONY: check-format
check-format:
	$(COMPOSE) build check-format-imports
	$(COMPOSE) run check-format-imports
	$(COMPOSE) build check-format
	$(COMPOSE) run check-format


.PHONY: style
style: check-format
	$(COMPOSE) build style
	$(COMPOSE) run style


.PHONY: complexity
complexity:
	$(COMPOSE) build complexity
	$(COMPOSE) run complexity

.PHONY: security-sast
security-sast:
	$(COMPOSE) build security-sast
	$(COMPOSE) run security-sast
