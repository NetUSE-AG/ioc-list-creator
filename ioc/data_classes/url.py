class Url:
    """Data class to hold information for a url
    """

    def __init__(self, url, domain, insert_date, source):
        """Constructor for class Url

        Args:
            ip (str): Url
            insert_date (str): Datetime of creation date
            source (str): Source of ip/file
        """
        self.url = url
        self.domain = domain
        self.insert_date = insert_date
        self.source = source

    def to_dict(self):
        """Returns instance as a dictionary

        Returns:
            Dict: Dictionary of instance
        """
        return {
            "url": self.url,
            "source": self.source,
            "domain": self.domain,
            "insert_date": self.insert_date
        }

    def __repr__(self):
        return str(self.url) + ';' + str(self.source) + ';' + str(self.domain) + ';' + str(self.insert_date)

    def __eq__(self, other):
        return self.url == other.url and self.domain == other.domain

    def __hash__(self):
        return hash((self.url + self.domain))