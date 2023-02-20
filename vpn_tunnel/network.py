import itertools


class OSPF:
    newid = itertools.count()

    def __init__(self, tag, ip, wildcard, area):
        self.id = next(OSPF.newid)
        self.tag = tag
        self.ip = ip
        self.wildcard = wildcard
        self.area = area

    def func(self):
        print("After calling func() method..")
        print("my tag is", self.tag)
        print("my ID is", self.id)
        print("My ip is", self.ip)
        print("My wildcardmask is", self.wildcard)
        print("My subnet is", self.area)
