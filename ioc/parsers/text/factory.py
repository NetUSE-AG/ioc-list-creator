from .parser import *

class TextFactory:
    """Factory class for text parsers
    """

    @staticmethod
    def create_text_parser(file):
        """Create parser for text file and return its data

        Args:
            file (json): text file to parse

        Returns:
            List: Data of file
        """
        if file['parser'] == "domain":
            return DomainParser.parse(file['path'], file['source'])
        elif file['parser'] == "ip":
            return IpParser.parse(file['path'], file['source'])
        elif file['parser'] == "url":
            return UrlParser.parse(file['path'], file['source'])
        elif file['parser'] == "pallebone":
            return PalleboneIpParser.parse(file['path'], file['source'])
        elif file['parser'] == "executemalware":
            return ExecutemalwareParser.parse(file['path'], file['source'])