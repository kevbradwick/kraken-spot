.PHONY: clean
clean:
	rm -rf htmlcov .coverage .pytest_cache

.PHONY: test
test: clean
ifndef COVERAGE
	poetry run python -m pytest -m "not integration"
else
	poetry run coverage run -m pytest -m "not integration"
	poetry run coverage html
	@echo "=============================================================================="
	@echo "||                                                                          ||"
	@echo "||                View HTML report http://localhost:8000                    ||"
	@echo "||                                                                          ||"
	@echo "=============================================================================="
	poetry run python -m http.server --directory htmlcov
endif

.PHONY: t
t: test

.PHONY: test-integration
test-integration:
	poetry run python -m pytest -m integration

.PHONY: fmt
fmt:
	poetry run autoflake --ignore-init-module-imports --remove-all-unused-imports --verbose --remove-unused-variables -r -i kraken_spot/*
	poetry run isort .
	poetry run black .

