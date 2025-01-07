from .parser import *

class JsonFactory:
    """Factory class for json parsers
    """

    @staticmethod
    def create_json_parser(file):
        """Create parser for text file and return its data

        Args:
            file (json): text file to parse

        Returns:
            List: Data of file
        """
        if file['parser'] == "cert-agid":
            return CertAgidParser.parse(file['path'], file['source'])