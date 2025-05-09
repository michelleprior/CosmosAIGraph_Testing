#!/bin/bash

# This script executes the complete set of Python code unit tests.
#
# Notes:
# 1) The Graph microservice should be running on localhost
#    when these tests are executed.
# 2) These tests use the "live" services (CosmosDB, Azure OpenAI, etc)
#    rather than fixtures or mocks.
# 3) Code coverage is generated and is useful in identifying dead
#    or untested code.
# 4) The pytest testing framework is used.
# 5) The test scripts are in the tests/ directory.
# 6) The following annotation can be used to disable a test:
#    @pytest.mark.skip(reason="This test is currently disabled.")
# 7) Individual tests can also be executed from the command line.
#    See the comments atop each test script, such as:
#    pytest -v tests/test_config_service.py
#
# Chris Joakim, Microsoft, 2025

# Create the tmp directory if it doesn't exist
mkdir -p ./tmp

# Remove all files in the tmp directory
rm -f ./tmp/*

# Execute unit tests with code coverage
echo 'Executing unit tests with code coverage...'
pytest -v --cov=src/ --cov-report html tests/
