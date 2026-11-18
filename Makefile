.PHONY: help install generate engine evaluate api ui test-all test-unit test-integration test-functional test-regression test-blackbox test-e2e

help:
	@echo "Hayah-Pulse targets:"
	@echo "  make install / generate / engine / evaluate / api / ui"
	@echo "  make test-all | test-unit | test-integration | test-functional"
	@echo "  make test-regression | test-blackbox | test-e2e"

install:
	python -m pip install -r backend/requirements.txt
	cd frontend && npm install

generate:
	python backend/scripts/generate_synthetic_cohort.py

engine:
	python backend/scripts/run_engine.py

evaluate:
	python backend/scripts/run_evaluation.py

api:
	python -m uvicorn app.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000

ui:
	cd frontend && npm run dev

test-unit:
	python -m pytest backend/tests/unit -q

test-integration:
	python -m pytest backend/tests/integration -q

test-functional:
	python -m pytest backend/tests/functional -q

test-regression:
	python -m pytest backend/tests/regression -q

test-blackbox:
	python -m pytest backend/tests/blackbox -q

test-e2e:
	python -m pytest backend/tests/e2e -q

test-all:
	python -m pytest backend/tests -q
