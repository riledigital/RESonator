OUTPUTS = build dist RESonatorGUI.spec

build: clean
	pyinstaller --clean --windowed --onefile --hidden-import cmath ./src/resonator/gui/RESonatorGUI.py RESonatorGUI.spec

.PHONY : clean
clean :
	rm -rf $(OUTPUTS)

.PHONY: test
test: clean
	pytest
