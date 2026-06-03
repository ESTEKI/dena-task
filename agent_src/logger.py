import os
import logging
import sys
COLOR_RESET = "\033[0m"
COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_GRAY = "\033[90m"

class ColoredFormatter(logging.Formatter):
        def format(self, record):
            timestamp = self.formatTime(record, self.datefmt)
            name_color = COLOR_BLUE
            level_color = {
                "DEBUG": COLOR_GRAY,
                "INFO": COLOR_GREEN,
                "WARNING": COLOR_YELLOW,
                "ERROR": COLOR_RED,
                "CRITICAL": COLOR_MAGENTA
            }.get(record.levelname, COLOR_RESET)

            formatted = (
                f"{timestamp} "
                f"{name_color}[{record.dynamic_name}]{COLOR_RESET} "
                f"{level_color}[{record.levelname}]{COLOR_RESET} "
                f"{record.getMessage()}"
            )
            return formatted
        
class LoggerManager:
    def __init__(self, log_filename: str, level=logging.INFO):
        if not log_filename.endswith(".log"):
            log_filename += ".log"

        log_path = os.path.join("logs", log_filename)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # IMPORTANT: unique logger per file
        self.logger = logging.getLogger(log_filename)
        self.logger.setLevel(level)
        self.logger.propagate = False

        plain_formatter = logging.Formatter(
            "%(asctime)s [%(dynamic_name)s] [%(levelname)s] %(message)s"
        )

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(plain_formatter)

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setFormatter(ColoredFormatter())

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def log(self, message: str, name: str = "default", level: str = "info"):
        extra = {"dynamic_name": name}
        level = level.lower()

        if level == "debug":
            self.logger.debug(message, extra=extra)
        elif level == "warning":
            self.logger.warning(message, extra=extra)
        elif level == "error":
            self.logger.error(message, extra=extra)
        elif level == "critical":
            self.logger.critical(message, extra=extra)
        else:
            self.logger.info(message, extra=extra)