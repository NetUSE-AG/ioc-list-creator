from ipaddress import ip_address

class Ip:
    """Data class to hold information for a ip
    """

    def __init__(self, ip, insert_date, source):
        """Constructor for class Ip

        Args:
            ip (str): Ip
            insert_date (str): Datetime of creation date
            source (str): Source of ip/file
        """
        self.ip = ip
        self.insert_date = insert_date
        self.source = source

    def to_dict(self):
        """Returns instance as a dictionary

        Returns:
            Dict: Dictionary of instance
        """
        return {
            "ip": self.ip,
            "insert_date": self.insert_date,
            "source": self.source
        }

    def __repr__(self):
        return str(self.ip) + ';' + str(self.source) + ';' + str(self.insert_date)

    def __eq__(self, other):
        return self.ip == other.ip

    def __hash__(self):
        return hash((self.ip))

    @staticmethod
    def is_private(ip):
        return ip_address(ip).is_private