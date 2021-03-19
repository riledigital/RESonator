OUTPUTS = build dist RESonatorGUI.spec

.PHONY: setup
setup:
	./init.sh

build: clean
	pyinstaller --clean --windowed --onefile --hidden-import cmath ./src/resonator/gui/RESonatorGUI.py RESonatorGUI.spec

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
