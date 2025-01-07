from .parser import *

class CsvFactory:
    """Factory class for csv parsers
    """

    @staticmethod
    def create_csv_parser(file):
        """Create parser for csv file and return its data

        Args:
            file (json): CSV file to parse

        Returns:
            List: Data of file
        """
        if file['parser'] == "cert":
            return CertPl.parse(file['path'], file['source'])
        elif file['parser'] == "abuse":
            return AbuseCh.parse(file['path'], file['source'])
