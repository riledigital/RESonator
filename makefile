OUTPUTS = build dist RESonatorGUI.spec cli.spec

.PHONY: setup
setup:
	./init.sh

.PHONY : clean
clean :
	rm -rf $(OUTPUTS) && poetry run pyclean -v .

.PHONY: test
test: clean
	poetry run pytest

.PHONY: docker-build
docker-build:
	docker build -t resonator .

.PHONY: docker-test
docker-test: docker-build
	./bin/test.sh

freeze-cli: clean
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages --log-level=WARN ./src/resonator/cli.py
