test:
	poetry run pytest

install:
	poetry install

package-install:
	python3 -m pip install --user dist/*.whl

# to install the same version again for testing behavior of installed app
package-reinstall:
	make build
	python3 -m pip install --user --force-reinstall dist/*.whl

build:
	poetry build

publish-test:
	poetry publish --dry-run
