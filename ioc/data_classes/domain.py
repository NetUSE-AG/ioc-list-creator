class Domain:
    """Data class to hold information for a domain
    """

    def __init__(self, domain, insert_date, source):
        """Constructor for class Domain

        Args:
            domain (str): Domain
            insert_date (str): Datetime of creation date
            source (str): Source of domain/file
        """
        self.domain = domain
        self.insert_date = insert_date
        self.source = source

    def to_dict(self):
        """Returns instance as a dictionary

        Returns:
            Dict: Dictionary of instance
        """
        return {
            "domain": self.domain,
            "insert_date": self.insert_date,
            "source": self.source
        }

    def __repr__(self):
        return str(self.domain) + ';' + str(self.source) + ';' + str(self.insert_date)

    def __eq__(self, other):
        return self.domain == other.domain

    def __hash__(self):
        return hash((self.domain))