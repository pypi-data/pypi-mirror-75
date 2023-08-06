import sys

LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3

LOG_LEVEL_TAGS = {
    LOG_LEVEL_ERROR: "ERROR",
    LOG_LEVEL_WARNING: "WARNING",
    LOG_LEVEL_INFO: "INFO",
    LOG_LEVEL_DEBUG: "DEBUG",
}


class Logger:
    def __init__(self, log_level):
        self.log_level = log_level

    def log(self, message, level):
        if level >= self.log_level:
            print(f"[{LOG_LEVEL_TAGS[level]}] {message}", file=sys.stderr)

        if level == LOG_LEVEL_ERROR:
            sys.exit(1)
