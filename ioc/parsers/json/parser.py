import validators
import json
from urllib.parse import urlparse
from datetime import datetime
from ioc.data_classes import Domain, Url, Ip

class CertAgidParser:
    @staticmethod
    def parse(text_file, source):
        data = {"ip": [], "domain": [], "url": []}

        with open(text_file, "r") as f:
            json_data = json.loads(f.read())
            json_data = list(json_data.values())[0]

        # 2021-12-23T10:49:45.094734+00:00
        last_update = datetime.strptime(json_data["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

        domains = json_data["ioc_list"]["domain"]
        urls = json_data["ioc_list"]["url"]
        ips = json_data["ioc_list"]["ipv4"]

        for ip in ips:
            if (validators.ipv4(ip.strip()) or validators.ipv6(ip.strip())) and not Ip.is_private(ip.strip()):
                data["ip"].append(Ip(ip.strip(), last_update.isoformat(), source))
        for url in urls:
            if validators.url(url.strip()):
                domain = urlparse(url.strip()).netloc
                data["url"].append(Url(url.strip(), domain, last_update.isoformat(), source))
        for domain in domains:
            if validators.domain(domain.strip()) or validators(domain.strip()):
                data["domain"].append(Domain(domain.strip(), last_update.isoformat(), source))

        return data

        
        