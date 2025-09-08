import json
import logging


class DefaultFormatter(logging.Formatter):
    def __init__(
        self,
        prefix: str | None = None,
        log_fmt: str | None = None,
        datefmt=None,
    ):
        super().__init__(datefmt=datefmt)
        self.log_fmt = (
            log_fmt
            or "%(asctime)s |%(levelname)s| [%(name)s] (%(module)s:%(lineno)d) - %(message)s"
        )
        self.prefix = prefix

    def format(self, record):
        if self.prefix:
            record.name = f"{self.prefix}.{record.name}"
        if getattr(record, "context", None) is not None:
            self.log_fmt += " | %(context)s"
        formatter = logging.Formatter(self.log_fmt, datefmt=self.datefmt)
        return formatter.format(record)


class JSONFormatter(DefaultFormatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "context": getattr(record, "context", None),
        }
        return json.dumps(log_record)


class ColorFormatter(DefaultFormatter):
    COLORS = {
        "DEBUG": "\033[37m",  # серый
        "INFO": "\033[36m",  # голубой
        "WARNING": "\033[33m",  # жёлтый
        "ERROR": "\033[31m",  # красный
        "CRITICAL": "\033[41m",  # красный фон
    }
    DATE_STYLE = "\033[1;33m"
    RESET = "\033[0m"

    def format(self, record):
        if "%(asctime)s" in self.log_fmt:
            self.log_fmt = self.log_fmt.replace(
                "%(asctime)s", f"{self.DATE_STYLE}%(asctime)s{self.RESET}"
            )
        if "%(levelname)" in self.log_fmt:
            self.log_fmt = self.log_fmt.replace(
                "%(levelname)s",
                f"{self.COLORS.get(record.levelname, self.RESET)}%(levelname)s{self.RESET}",
            )
        formatter = logging.Formatter(self.log_fmt, datefmt=self.datefmt)
        return formatter.format(record)
