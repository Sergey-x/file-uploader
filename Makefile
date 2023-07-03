APPLICATION_NAME = file_uploader
TEST = pytest -c pytest.ini $(APPLICATION_NAME)/tests/  --verbosity=2 --showlocals --log-level=DEBUG

install:
	poetry install

run:  ##@Application Run application server
	uvicorn $(APPLICATION_NAME).main:app --reload --port=3457

test:
	$(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	$(TEST) --cov=$(APPLICATION_NAME) --cov-fail-under=70

format:
	isort .

lint:
	isort --check . && \
	flake8 . --count --statistics

env:
	cp .env.example .env
