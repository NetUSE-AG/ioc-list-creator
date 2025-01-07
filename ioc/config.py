from configparser import ConfigParser
from pathlib import Path


class Config:
    """
    Class holds all config information needed for the programm
    """

    def __init__(self, config_file):
        """Constructor for class Config

        Args:
            config_file (Path): Path object for config file

        Raises:
            FileNotFoundError: Download file not found
        """
        config = ConfigParser()
        config.read(config_file)
        self.token = config['ioc']['token']
        self.download_list = Path(config['ioc']['download_list'])
        
        self.output_dir = Path(config['ioc']['output_dir'])
        self.output_ip_filename = "ip_blocklist.csv"
        self.output_domain_filename = "domain_blocklist.csv"
        self.output_url_filename = "url_blocklist.csv"

        if not self.download_list.exists() or not self.download_list.is_file():
            raise FileNotFoundError(
                f"Can't open file {self.download_list}. Either it doesn't exist or isn't a file")
        if not self.output_dir.exists() or not self.output_dir.is_dir():
            self.output_dir.mkdir()
            print(f"Created not existing directory {self.output_dir}")
