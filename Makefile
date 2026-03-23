# Makefile
.PHONY: test test-all test-slow test-cov clean

test:
	pytest -m "not slow" -v

test-all:
	pytest -v

test-slow:
	pytest -m slow -v

test-cov:
	pytest --cov=app.main --cov-report=term --cov-report=html -m "not slow"
	@echo "Relatório HTML gerado em htmlcov/index.html"

clean:
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true