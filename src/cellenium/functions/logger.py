from dataclasses import dataclass
from functools import cached_property
from typing import Literal

import logfire

from cellenium.settings import get_config

LogLevel = Literal["info", "error", "debug", "warning", "fatal"]


@dataclass
class Logger:

    name: str

    @cached_property
    def config(self):
        # Configured on first log call so module-level loggers don't load settings at import time.
        return logfire.configure(
            token=get_config().LOGFIRE_TOKEN,
            send_to_logfire="if-token-present",
        )

    def fire(self, message: str, level: LogLevel | None = 'info', **attributes: object) -> None:
        with self.config.span(self.name):
            match level:
                case "info":
                    self.config.info(message, **attributes)
                case "error":
                    self.config.error(message, **attributes)
                case "debug":
                    self.config.debug(message, **attributes)
                case "warning":
                    self.config.warning(message, **attributes)
                case "fatal":
                    self.config.fatal(message, **attributes)
                case _:
                    self.config.info(message, **attributes)


if __name__ == "__main__":
    logger = Logger(name="app")
    logger.fire(message="hi")
