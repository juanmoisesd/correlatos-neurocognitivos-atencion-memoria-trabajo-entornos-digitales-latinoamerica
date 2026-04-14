.PHONY: all test clean run

all: setup run test

setup:
	pip install -r requirements.txt

run:
	bash run.sh

test:
	pytest tests/

clean:
	rm -rf __pycache__ .pytest_cache
