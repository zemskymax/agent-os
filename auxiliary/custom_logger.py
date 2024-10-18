#!/usr/bin/env python3
# import logging # no need for now

CRITICAL = 50
ERROR = 40
WARNING = 30
TOOLS_INFO = 22
USER_INPUT_INFO = 21
INFO = 20
DEBUG = 10
NOTSET = 0

class CustomLogger:
    def __init__(self, default_log_level = INFO):
        self.default_log_level = default_log_level

    def _set_color(self, log_string, log_level = None):
        color_levels = {
            10: "\033[36m{}\033[0m",        # DEBUG
            20: "\033[32m{}\033[0m",        # INFO
            22: "\033[35;40m{}\033[0m",     # TOOLS_INFO
            21: "\033[34;40m{}\033[0m",     # USER_INPUT_INFO
            30: "\033[33m{}\033[0m",        # WARNING
            40: "\033[31m{}\033[0m",        # ERROR
            50: "\033[7;31;31m{}\033[0m"    # FATAL/CRITICAL/EXCEPTION
        }
        if not log_level:
            return color_levels[20].format(log_string)
        else:
            return color_levels[int(log_level)].format(log_string)

    def print_log(self, log_string = "", log_level = INFO):
        if log_level < self.default_log_level or log_level is NOTSET:
            return

        if log_string:
            log_string = self._set_color(log_string, log_level)
            print(log_string)

if __name__ == "__main__":
    logger = CustomLogger(default_log_level=INFO)

    logger.print_log("debug", log_level=DEBUG)
    logger.print_log("info", log_level=INFO)
    logger.print_log("warning", log_level=WARNING)
    logger.print_log("error", log_level=ERROR)
    logger.print_log("critical", log_level=CRITICAL)
