TESTS_DIR := tests
COVERAGE_REPORT_TYPE := html
NOSE2_ARGS := --pretty-assert

init:
	pip3 install -r requirements.txt

test:
	nose2 --start-dir $(TESTS_DIR) $(NOSE2_ARGS)

test_coverage:
	nose2 --start-dir $(TESTS_DIR) --with-coverage

test_coverage_report:
	nose2 --start-dir $(TESTS_DIR) --with-coverage --coverage-report $(COVERAGE_REPORT_TYPE)

clean:
	rm -rf .coverage htmlcov