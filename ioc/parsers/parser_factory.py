from ioc.parsers.text import TextFactory
from ioc.parsers.csv import CsvFactory
from ioc.parsers.json import JsonFactory

class ParserFactory:
    """Factory Class for Parsers"""

    @staticmethod
    def create_parser(file):
        """Creates parser for file and returns its data

        Args:
            file (json): File to parse

        Returns:
            List: Data from file
        """
        if file['type'] == "text/plain":
            return TextFactory.create_text_parser(file)
        elif file['type'] == "text/csv":
            return CsvFactory.create_csv_parser(file)
        elif file['type'] == "text/json":
            return JsonFactory.create_json_parser(file)