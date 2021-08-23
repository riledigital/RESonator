from resonator.web.app import create_app
import multiprocessing
import gunicorn.app.base
from webbrowser import open as open_browser


def number_of_workers():
    return 1
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        "bind": "%s:%s" % ("0.0.0.0", 8089),
        "workers": number_of_workers(),
    }
    connection_str = f"http://{options['bind']}"
    print(f"Opening your browser to: {connection_str}")
    open_browser(connection_str)
    handler_app = create_app()
    StandaloneApplication(handler_app, options=options).run()
