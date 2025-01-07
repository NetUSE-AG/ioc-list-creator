import validators
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
from ioc.data_classes import Domain, Url, Ip


class DomainParser:
    """Parser for text files with domains
    """

    @staticmethod
    def parse(text_file, source):
        """Parses data from text file

        Args:
            csv_file (Path): text file to parse
            source (str): Source of file

        Returns:
            List[Domain]: Data of file
        """
        data = list()
        with open(text_file, 'r') as f:
            for line in f:
                if validators.domain(line.strip()) or validators.url(line.strip()):
                    data.append(Domain(line.strip(), "", source))
        return data

class UrlParser:
    """Parser for text files with urls
    """

    @staticmethod
    def parse(text_file, source):
        """Parses data from text file

        Args:
            csv_file (Path): text file to parse
            source (str): Source of file

        Returns:
            List[Url]: Data of file
        """
        data = list()
        with open(text_file, 'r') as f:
            for line in f:
                if validators.url(line.strip()):
                    domain = urlparse(line.strip()).netloc
                    data.append(Url(line.strip(), domain, "", source))
        return data

class IpParser:
    """Parser for text files with ips
    """

    @staticmethod
    def parse(text_file, source):
        """Parses data from text file

        Args:
            csv_file (Path): text file to parse
            source (str): Source of file

        Returns:
            List[Ip]: Data of file
        """
        data = list()
        with open(text_file, 'r') as f:
            for line in f:
                if (validators.ipv4(line.strip()) or validators.ipv6(line.strip())) and not Ip.is_private(ip.strip()):
                    data.append(Ip(line.strip(), "", source))
        return data


class PalleboneIpParser:
    """Parser for text files from Pallebone with IPs to parse only last seven days.
    """

    @staticmethod
    def parse(text_file, source):
        """Parses IPs from last seven days from text file

        Args:
            text_file (Path): text file to parse
            source (str): Source of file

        Returns:
            List[Ip]: Data of last seven days
        """
        regex = re.compile(r"\b\w{1,4}\s\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}")

        found_dates = list()
        valid_dates = list()
        data = list()

        today = datetime.today().date()
        first = today - timedelta(days=7)

        with open(text_file, "r") as f:
            lines = f.readlines()

            # use regex to find dates and line numbers in file
            for number, line in enumerate(lines, 1):
                search = regex.search(line)
                if search:
                    found_dates.append((number, search.group(0)))
            found_dates.reverse()

            # check each found date if its in the last seven days or older
            for line, found_date in found_dates:
                parsed_date = datetime.strptime(found_date, "%b %d %H:%M:%S")
                if parsed_date.month <= today.month:
                    parsed_date = parsed_date.replace(year=today.year)
                else:
                    parsed_date = parsed_date.replace(year=today.year-1)

                if today >= parsed_date.date() >= first:
                    valid_dates.append((line, parsed_date))
            
            # extract ips for last seven dates from file
            last_line = len(lines)
            for line, date in valid_dates:
                for ip in lines[line:last_line]:
                    if (validators.ipv4(ip.strip()) or validators.ipv6(ip.strip())) and not Ip.is_private(ip.strip()):
                        data.append(Ip(ip.strip(), date.isoformat(), source))
                last_line = line
            return data
			
class ExecutemalwareParser:
    @staticmethod
    def parse(text_file, source):
        def check(line):
            if (validators.ipv4(line) or validators.ipv6(line)) and not Ip.is_private(line):
                return "ip"
            elif validators.domain(line):
                return "domain"
            elif validators.url(line):
                return "url"
            else:
                return None
				
        data={"ip":[],"domain":[],"url":[]}
        for line in list(open(text_file).read().split("\n")):
            column = check(line)
            if column is not None:
                data[column].append(line.strip())
	
        data["ip"] = [Ip(data_cell, "", source) for data_cell in data["ip"]]
        data["domain"] = [Domain(data_cell, "", source) for data_cell in data["domain"]]
        data["url"] = [Url(data_cell, urlparse(data_cell).netloc, "", source) for data_cell in data["url"]]
        
		
        return data