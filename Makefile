install:
	pip3 install -r requirements.txt -e .

install-dev:
	pip3 install -r requirements.txt -e ".[dev]"

flake8-lint:
	flake8 whispers/ tests/

isort-lint:
	isort --check-only whispers/ tests/

black-lint:
	black --check whispers/ tests/

lint: isort-lint black-lint flake8-lint

format:
	autoflake --in-place --recursive --remove-all-unused-imports whispers/ tests/
	autopep8 --in-place --recursive --aggressive --aggressive whispers/ tests/
	isort whispers/ tests/
	black whispers/ tests/

unit:
	pytest --show-capture=all -v tests/

coverage:
	coverage run --source=whispers/ --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage xml -i -o build/coverage.xml
	coverage report
	coverage-badge -f -o coverage.svg

test: 
	make lint coverage

build-image:
	python3 -m build
	docker build -t=whispers --rm=true . 
	# docker rmi -f $$(docker images --filter "dangling=true" -q --no-trunc)

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" \
	pip-compile \
		--no-emit-index-url \
		--output-file requirements.txt \
		--no-annotate \
		--strip-extras \
		--no-allow-unsafe \
		setup.py

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze-upgrade" \
	pip-compile \
		--no-emit-index-url \
		--output-file requirements.txt \
		--no-annotate \
		--strip-extras \
		--no-allow-unsafe \
		--upgrade \
		setup.py

publish:
	python3 setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*

test-pip:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps whispers

.PHONY: install install-dev isort-lint black-lint flake8-lint format lint unit coverage test publish build-image
