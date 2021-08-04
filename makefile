OUTPUTS = build dist RESonatorGUI.spec cli.spec

.PHONY: setup
setup:
	./init.sh

.PHONY : clean
clean :
	rm -rf $(OUTPUTS)

.PHONY: test
test: clean
	pytest

.PHONY: docker-build
docker-build:
	docker build -t resonator .

.PHONY: docker-test
docker-test: docker-build
	./bin/test.sh

freeze-cli:
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages ./src/resonator/cli.py
