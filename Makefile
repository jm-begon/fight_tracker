check: lint test

test:
	pytest .

lint:
	pre-commit run --all-files


# TODO doc
