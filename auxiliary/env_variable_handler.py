import os
from auxiliary.custom_logger import *


class EnvironmentVariableHandler:
    def __init__(self):
        self.logger = CustomLogger()

    def get_from_env(self, env_key: str) -> str:
        """Get a value from the environment variable.

        Args:
            env_key: The environment variable to look up if the key is not
                in the dictionary.

        Returns:
            str: The value of the environment variable.

        """
        if env_key in os.environ and os.environ[env_key]:
            return os.environ[env_key]

        self.logger.print_log(f"\nDid not find {env_key}, please add this environment variable!\n", ERROR)

        return ""
