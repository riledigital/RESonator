build:
	pyinstaller --clean --windowed --onefile ./resonator/gui/RESonatorGUI.py RESonatorGUI.spec

.PHONY : clean
clean :
	rm -rf build dist $(objects)
