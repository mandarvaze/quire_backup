.PHONY: dev
dev:
	@poetry run python quire_backup/run.py

# Testing and linting targets
.PHONY: lint
lint:
	@flake8

.PHONY: format
format:
	@autopep8 -r --in-place --aggressive quire_backup

# anything, in regex-speak
filter = "."

# additional arguments for pytest
unit_test_all = "false"
ifeq ($(filter),".")
	unit_test_all = "true"
endif
ifdef path
	unit_test_all = "false"
endif
# We don't want functional tests on CI
pytest_args = tests -s -v -k $(filter)
coverage_args = ""
ifeq ($(unit_test_all),"true")
	coverage_args = --cov=quire_backup --cov-branch --cov-report html --cov-report xml:cov.xml --cov-report term-missing --cov-fail-under=80
endif

.PHONY: unit
unit:
ifndef path
	@poetry run pytest $(coverage_args) $(pytest_args)
else
	@poetry run pytest
endif

.PHONY: tests
# tests: format lint types unit
tests: format lint unit

.PHONY: clean
clean:
	@rm -rf .coverage .mypy_cache htmlcov/ htmltypecov typecov xunit.xml \
			.git/hooks/pre-commit .git/hooks/pre-push
	@rm -f .installed cov.xml
	@rm -f *.log
