.PHONY: setup index run test

setup:
	uv venv && . .venv/bin/activate && uv pip install -e .

index:
	python scripts/build_index.py
	python scripts/bootstrap_image_map.py

run:
	uvicorn src.app.main:app --reload

test:
	pytest -q
