from argparse import ArgumentParser
from pathlib import Path
from ioc import Config, Downloader, Parser

import tempfile


def parse_args():
    """Function parses command line arguments

    Raises:
        FileNotFoundError: Wrong file type for config file
        FileNotFoundError: Config file not found

    Returns:
        Path: Config file Path object
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, default=Path("ioc-lists.conf"), help="Specify the used config file. If "
                        "none is given the default "
                        "ioc-lists.conf is "
                        "used.")
    args = parser.parse_args()

    if args.config:
        if not args.config.name.endswith(".conf"):
            raise FileNotFoundError("Config file has wrong type. Aborting!")
        if not args.config.exists() or not args.config.is_file():
            raise FileNotFoundError(f"Couldn't find {args.config}. Aborting!")

    return args.config


if __name__ == "__main__":
    config = Config(parse_args())
    download_dir = tempfile.TemporaryDirectory()

    downloader = Downloader(config.download_list, download_dir)
    parser = Parser(config.output_dir, config.output_ip_filename, config.output_domain_filename, config.output_url_filename)

    downloader.download_files()
    parser.read_files(downloader.files)
    parser.save_to_csv()

    download_dir.cleanup()
