# poetry run python -m time_tracker -s Task1
# poetry run pytest

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

# to install the same version again
# rebuild before installing
package-reinstall:
	make build
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 brain_games

test:
	poetry run pytest