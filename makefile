OUTPUTS = build dist RESonatorGUI.spec cli.spec
export FLASK_APP=./resonator.web.app
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
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages --log-level=WARN -n resonator-cli ./resonator/cli.py

freeze-webgui: clean
	poetry run pyinstaller --clean --add-data="resonator/web/templates:./templates" --paths=.venv/lib/python3.9/site-packages --log-level=WARN -c -n resonator-web-gui ./resonator/web/app.py \
	&& cd dist \
	&& tar -C ./dist -cvzf RESonator-build.tar.gz resonator-web-gui

serve: 
	poetry run flask run --host='0.0.0.0' --cert=adhoc

run-prod-server: clean
	poetry run gunicorn resonator.web.app:app
