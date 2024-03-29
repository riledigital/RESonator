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
	poetry run pyinstaller --clean --paths=.venv/lib/python3.9/site-packages --log-level=WARN -n resonator-cli ./resonator/cli.py

freeze-webgui: clean
	poetry install \
	&& poetry run pyinstaller \
	--clean \
	--add-data="resonator/web/templates:./templates" \
	--add-data="README.md:." \
	--paths=.venv/lib/python3.9/site-packages \
	--log-level=WARN \
	-c -n resonator-web-gui \
	--onefile \
	./resonator/web/app.py \
	&& tar -C ./dist -cvzf ./dist/RESonator-build.tar.gz resonator-web-gui

serve:
	export FLASK_APP=./resonator.web.app \
	&& export FLASK_ENV=development \
	&& poetry run flask run --host='0.0.0.0' 

run-prod-server: clean
	poetry run gunicorn resonator.web.app:app
