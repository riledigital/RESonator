OUTPUTS = build dist RESonatorGUI.spec cli.spec
export FLASK_APP=./src/resonator.web.app
export FLASK_ENV=development

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
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages --log-level=WARN -n resonator-cli ./src/resonator/cli.py

freeze-webgui: clean
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages --log-level=WARN -n resonator-web-gui ./src/resonator/web/app.py

serve: 
	poetry run flask run --host='0.0.0.0' --cert=adhoc
