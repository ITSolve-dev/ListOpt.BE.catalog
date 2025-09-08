from catalog.infrastructure.executable import ExecutableProtocol


class Runner:
    _http_app: ExecutableProtocol

    def __init__(self, http_app: ExecutableProtocol) -> None:
        self._http_app = http_app

    def run(self):
        self._http_app.run()
