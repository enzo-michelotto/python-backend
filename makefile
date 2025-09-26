
PYTHON := python3
SRC    := utils
COVERAGE := 90

.PHONY: all lint type test bandit clean

all: lint type test bandit

lint:
	$(PYTHON) -m ruff check . --fix

format:
	$(PYTHON) -m ruff format .

type:
	$(PYTHON) -m mypy $(SRC)

test:
	$(PYTHON) -m pytest --cov=$(SRC) --cov-fail-under=$(COVERAGE)

bandit:
	$(PYTHON) -m bandit -c .bandit.yaml -r app


clean:
	rm -rf .pytest_cache .mypy_cache __pycache__ .coverage public/coverage
