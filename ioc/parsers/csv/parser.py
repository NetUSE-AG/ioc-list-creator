import csv
from datetime import datetime
from ioc.data_classes import Domain, Ip


class CertPl:
    """Parser for csv files from cert.pl"""

    @staticmethod
    def parse(csv_file, source):
        """Parses data from csv file

        Args:
            csv_file (Path): CSV file to parse
            source (str): Source of file

        Returns:
            List[Domain]: Data of file
        """
        data = list()
        with open(csv_file, "r") as f:
            lines = f.read().splitlines()[1:]
            csv_reader = csv.reader(lines, delimiter="\t")
            for row in csv_reader:
                data.append(Domain(row[1].strip(), row[2].strip(), source))
        return data

class AbuseCh:
    """Parser for csv files from abuse.AbuseCh
    """

    @staticmethod
    def parse(csv_file, source):
        """Parses data from csv file

        Args:
            csv_file (Path): CSV file to parse
            source (str): Source of file

        Returns:
            List[IP]: Data of file
        """
        data = list()
        with open(csv_file, "r") as f:
            lines = f.read().splitlines()[9:-1]
            csv_reader = csv.reader(lines, delimiter=",")
            for row in csv_reader and not Ip.is_private(row[1].strip()):
                data.append(Ip(row[1].strip(), datetime.strptime(row[0].strip(), "%Y-%m-%d %H:%M:%S").isoformat(), source))
        return data
