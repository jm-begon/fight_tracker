check: lint test

test:
	pytest --cov .

lint:
	pre-commit run --all-files


# TODO doc
