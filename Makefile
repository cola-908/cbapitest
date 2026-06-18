.PHONY: setup test-smoke test-flow test-integration test-all test-report clean

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	cp -n .env.example .env || true

test-smoke:
	.venv/bin/pytest -m smoke -v

test-flow:
	.venv/bin/pytest -m flow -v

test-integration:
	.venv/bin/pytest -m integration -v

test-all:
	.venv/bin/pytest -v --alluredir=reports/allure-results

test-report:
	.venv/bin/allure serve reports/allure-results

clean:
	rm -rf reports/allure-results
	find . -type d -name __pycache__ -exec rm -rf {} +
