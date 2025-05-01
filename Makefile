help:
clean:
	rm -rf dist target coverage sample htmligator-0.1.0.tar.gz
run:
	rm -f tests/test-data/sample1.html tests/test-data/sample1/*.html tests/test-data/sample1.zip
	poetry run htmligator tests/test-data/sample1
	unzip -t tests/test-data/sample1.zip
build:
	scripts/set-version.sh
	poetry build
install:
	poetry install
flake8:
	poetry run flake8
update:
	poetry update
test:
	 poetry run pytest --capture=sys \
	 --junit-xml=coverage/test-results.xml \
	 --cov=htmligator \
	 --cov-report term-missing  \
	 --cov-report xml:coverage/coverage.xml \
	 --cov-report html:coverage/coverage.html \
	 --cov-report lcov:coverage/coverage.info

all: clean install flake8 build test

release:
	scripts/release.sh

commit:
	scripts/git-commit.sh
