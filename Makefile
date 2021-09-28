.PHONY: pip_dev dev lint test test_unit pip_test_integration test_integration clean clean_test_integration

env pip_dev:
	python3.8 -m venv env
	env/bin/pip3.8 install --upgrade pip
	env/bin/pip3.8 install -r requirements-dev.txt

dev: env
	env/bin/python3.8 dev.py

lint: env
	env/bin/flake8 api/ tests/ dev.py application.py

test: env
	env/bin/py.test tests/unit/

test_unit: env
	env/bin/py.test \
		--cov api tests/unit/ \
		--cov-report xml \
		--junitxml=pyunit.xml

tests/integration/env pip_test_integration:
	python3.8 -m venv tests/integration/env
	tests/integration/env/bin/pip3.8 install --upgrade pip
	tests/integration/env/bin/pip3.8 install -r tests/integration/requirements.txt
	
test_integration: tests/integration/env
	tests/integration/env/bin/py.test tests/integration

clean:
	rm -rf env

clean_test_integration:
	rm -rf tests/integration/env
