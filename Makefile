check: lint test

test:
	pytest --cov .

lint:
	black .
	isort .
	mypy .


requirements:
	pip-compile dev-requirements.in
	pip-sync dev-requirements.txt
	pip install -r dev-requirements.txt
	pip install -e .

# TODO doc
