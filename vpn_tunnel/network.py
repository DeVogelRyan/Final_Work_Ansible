import itertools


class Network:
    newid = itertools.count()

    def __init__(self, *args):
        # DHCP
        if len(args) == 3:
            self.id = next(Network.newid)
            self.tag = args[1]
            self.network = args[2]
            self.subnet = args[3]
        # OSPF
        elif len(args) == 4:
            self.id = next(Network.newid)
            self.tag = args[1]
            self.network = args[2]
            self.wildcard = args[3]
            self.area = args[4]
