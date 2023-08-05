from libifstate.link.base import Link
from libifstate.exception import LinkCannotAdd

class PhysicalLink(Link):
    def __init__(self, name, link, ethtool):
        super().__init__(name, link, ethtool)
        self.cap_create = False
        self.cap_ethtool = True
        self.ethtool = ethtool
 
    def create(self):
        raise LinkCannotAdd()
