TESTS_DIR := tests
# Declare the TESTS_DIR directory as a phony -> `make` will ignore it (and run the
# 'tests' rule if TESTS_DIR == tests.
.PHONY: $(TESTS_DIR)
COVERAGE_DIR_TO_TEST := heuristics
COVERAGE_CONFIG_FILE := .coveragerc
COVERAGE_REPORT_TYPE := html
COVERAGE_OUTPUT_DIR := coverage_html_report
NOSE2_ARGS := --start-dir $(TESTS_DIR)

init:
	pip3 install -r requirements.txt

tests:
	nose2 $(NOSE2_ARGS)

tests_coverage:
	nose2 $(NOSE2_ARGS) \
		--with-coverage

tests_coverage_report:
	nose2 $(NOSE2_ARGS) \
		--with-coverage \
		--coverage-config $(COVERAGE_CONFIG_FILE) \
		--coverage-report $(COVERAGE_REPORT_TYPE) \
		--coverage $(COVERAGE_DIR_TO_TEST)

clean:
	rm -rf .coverage $(COVERAGE_OUTPUT_DIR)