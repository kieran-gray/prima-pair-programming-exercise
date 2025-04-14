format:
	uv run ruff format src
	uv run ruff check src --fix

lint:
	uv run mypy src
	uv run ruff check src
	uv run ruff format src --check

test:
	uv run pytest --cov
