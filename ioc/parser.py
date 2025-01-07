from pathlib import Path
from concurrent import futures
from .parsers import ParserFactory

class Parser:
    """Class for handling all file parsing
    """

    def __init__(self, output_dir, output_ip_filename, output_domain_filename, output_url_filename):
        """Constructor for class Parser

        Args:
            output_dir (Path): Folder to save csv files to
            output_ip_filename (str): Filename for IP csv file
            output_domain_filename (str): Filename for domain csv file
            output_url_filename (str): Filename for url csv file
        """
        self.output_dir = output_dir
        self.output_ip_filename = output_ip_filename
        self.output_domain_filename = output_domain_filename
        self.output_url_filename = output_url_filename
        self.domains = []
        self.ips = []
        self.urls = []

    def _parse_file(self, file):
        """Internal function to parse a single file and save its data to

        Args:
            file (json): File to parse
        """
        #print(f"\t[+]\tParsing {file['path']}")
        if file['content'] == 'domain':
            self.domains += ParserFactory.create_parser(file)
        if file['content'] == 'url':
            self.urls += ParserFactory.create_parser(file)
        if file['content'] == 'ip':
            self.ips += ParserFactory.create_parser(file)
        if file['content'] == 'multi':
            Data = ParserFactory.create_parser(file)
            self.domains += Data['domain']
            self.urls += Data['url']
            self.ips += Data['ip']

    def read_files(self, files):
        """Function to parse all downloaded files.
        Spawns a thread for each individual file

        Args:
            files (List): List of files to parse
        """
        #print("[^]\tParsing downloaded files")
        with futures.ThreadPoolExecutor(max_workers=5) as e:
            for file in files:
                e.submit(self._parse_file, file)
        #print("[^]\tParsing files completed")       

    def save_to_csv(self):
        """
        Function to save all data to individual csv files
        """
        with open(self.output_dir/self.output_domain_filename, 'w+') as f:
            f.write('domain;source;insert_date\n')
            # for domain in set(sorted(self.domains, key=lambda d: (d.domain, d.insert_date)))
            # sort by insert_date descending, remove duplicates, sort by domain ascending (don't ask...)
            for domain in sorted(set(sorted(self.domains, key=lambda d: d.insert_date, reverse=True)), key=lambda d: d.domain, reverse=False):
                f.write(str(domain) + '\n')

        with open(self.output_dir/self.output_ip_filename, 'w+') as f:
            f.write('ip;source;insert_date\n')
            # sort by insert_date descending, remove duplicates, sort by ip ascending (don't ask...)
            for ip in sorted(set(sorted(self.ips, key=lambda d: d.insert_date, reverse=True)), key=lambda d: d.ip, reverse=False):
                f.write(str(ip) + '\n')

        with open(self.output_dir/self.output_url_filename, 'w+') as f:
            f.write('url;source;domain;insert_date\n')
            # sort by insert_date descending, remove duplicates, sort by url ascending (don't ask...)
            for url in sorted(set(sorted(self.urls, key=lambda d: d.insert_date, reverse=True)), key=lambda d: d.url, reverse=False):
                f.write(str(url) + '\n')
