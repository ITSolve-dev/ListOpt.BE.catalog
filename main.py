import logging
import logging.config

from catalog.infrastructure.di import Container

container = Container()
logging.config.dictConfig(container.log_config())

# only for running uvicorn
http_app = container.http_app()


if __name__ == "__main__":
    runner = container.runner()
    runner.run()
