check: lint test

test:
	PYTHONPATH="fight_tracker/" pytest .

lint:
	pre-commit run --all-files


# TODO doc
