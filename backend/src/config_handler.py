import my_config
import configparser


class ConfigHandler():
    def __init__(self, config_path=my_config.CONFIG_PATH):
        self._config_path = config_path

    def get_chain_config(self, section, key):
        config = configparser.ConfigParser()
        config.read(self._config_path)
        return config.get(section, key)
