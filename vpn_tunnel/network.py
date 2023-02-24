import itertools


class Network:
    newid = itertools.count()

    def __init__(self, *args):
        # DHCP
        if len(args) == 3:
            self.id = next(Network.newid)
            self.tag = args[0]
            self.network = args[1]
            self.subnet = args[2]
        # OSPF
        elif len(args) == 4:
            self.id = next(Network.newid)
            self.tag = args[0]
            self.network = args[1]
            self.wildcard = args[2]
            self.area = args[3]
