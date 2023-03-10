import os
from network import Network
from basic_functions import *


def getBannerMessages(TAG: str):
    bannerMessage = input(f"[{TAG}] Banner message: ")
    if (len(bannerMessage) > 0):
        # Open a file in append mode
        file = open('./ansible/variables.yml', 'a')
        file.write(f"\n{TAG}_banner: '{bannerMessage}'")  # Write some text
        file.close()  # Close the file
    else:
        getBannerMessages(TAG)


def getDetailsDHCP(DHCPList: list, TAG: str):
    print("setup DHCP...")
    # strip() removes any spaces that might have been added.
    pool = input(f"[{TAG}] Pool name: ").strip()
    defaultRouter = input(f"[{TAG}] Default-router: ")
    subnet = input(
        f"[{TAG}] Subnet mask(ex. 255.255.255.0) for Default-router: ")
    print("Let's now choose an interface for the Default-Router. Here is a list: ")
    # Here we run show ip interface brief on the given host.
    os.system(f"ansible {TAG} -m raw -a 'show ip int brief' -u cisco -k")
    interface = input(f"[{TAG}] Interface for default-router: ")
    # Checking if all the details are valid. Else we ask to fill it in again.
    if (valid_ip_address(defaultRouter) == False or valid_ip_address(subnet) == False or len(pool) == 0 or len(interface) == 0):
        print("One of the inputs was wrong let's start again.")
        getDetailsDHCP(DHCPList, TAG)
        return
    WriteDHCPToFile(pool, defaultRouter, subnet, interface, TAG)
    getDHCPNetworks(DHCPList, TAG)


def getDHCPNetworks(DHCPList: list, TAG: str):
    network = input(f"[{TAG}] Network address: ")
    subnet = input(f"[{TAG}] Subnet mask(ex. 255.255.255.0): ")
    # Checking if all the details are valid. Else we ask to fill it in again.
    if (valid_ip_address(network) == False or valid_ip_address(subnet) == False):
        print("One of the inputs was wrong let's start again.")
        getDHCPNetworks(DHCPList, TAG)
        return
    # adding our class to a list
    DHCPList.append(Network(TAG, network, subnet))
    WriteDHCPListToFile(DHCPList, TAG)


def WriteDHCPToFile(pool: str, defaultRouter: str,  subnet: str, interface: str, TAG: str):
    file = open('./ansible/variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nDHCP_Pool_{TAG}: {pool}')  # Write some text
    file.write(f'\nDHCP_Default_Router_{TAG}: {defaultRouter}')
    file.write(f'\nDHCP_Default_Router_Subnet_{TAG}: {subnet}')
    file.write(f'\nDHCP_Default_Router_Interface_{TAG}: {interface}')
    file.close()  # Close the file


def WriteDHCPListToFile(DHCPList: list, TAG: str):
    file = open('./ansible/variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nDHCPNetwork_{TAG}:')  # Write some text
    # Looping over the given list with objects that look like the following:
    # {
    # DHCPNetwork_R1:
    # network0:
    # ip: 192.168.1.0
    # subnet: 255.255.255.0
    # }
    for item in DHCPList:
        file.write(f'\n  network{item.id}:')  # Write some text
        file.write(f'\n    ip: {item.network}')
        file.write(f'\n    subnet: {item.subnet}')
    file.close()  # Close the file


def getOSPFdetails(OSPFList: list, TAG: str):
    print("setup a network for OSPF...")
    network = input(f"[{TAG}] Network address: ")
    wildcard = input(f"[{TAG}] Wildcard mask(ex. 0.0.0.255): ")
    area = input(f"[{TAG}] Area: ")
    # Checking if all the details are valid. Else we ask to fill it in again.
    if valid_ip_address(network) == False or valid_ip_address(wildcard) == False or not area.isnumeric():
        print("One of the inputs was wrong let's start again.")
        getOSPFdetails(OSPFList, TAG)
        return
    # adding our class to a list
    OSPFList.append(Network(TAG, network, wildcard, area))
    if Menu(f"Do you want to configure another OSPF network for {TAG}") == True:
        getOSPFdetails(OSPFList, TAG)
        return


def writeNetworksToFile(OSPFList: list, TAG: str):
    file = open('./ansible/variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nOSPFNetwork_{TAG}:')  # Write some text
    # Looping over the given list with objects that look like the following:
    # {
    # R1network:
    # network0:
    # ip: 192.168.1.0
    # wildcardMask: 0.0.0.255
    # area: 0
    # }
    for item in OSPFList:
        file.write(f'\n  network{item.id}:')  # Write some text
        file.write(f'\n    ip: {item.network}')
        file.write(f'\n    wildcardMask: {item.wildcard}')
        file.write(f'\n    area: {item.area}')
    file.close()  # Close the file


def getVPNDetails():
    tunnelSource = input("[R1] Tunnel source: ")
    tunnelDestination = input("[R1] Tunnel destination: ")
    R1tunnelIP = input("[R1] Tunnel ip address: ")
    R2tunnelIP = input("[R2] Tunnel ip address: ")
    if (checkIP(tunnelSource) == False or checkIP(tunnelDestination) == False
            or checkIP(R1tunnelIP) == False or checkIP(R2tunnelIP) == False):
        getVPNDetails()
        return
    else:
        writeVPnDetailsToFile(R1tunnelIP, R2tunnelIP,
                              tunnelSource, tunnelDestination)


def writeVPnDetailsToFile(R1tunnelIP, R2tunnelIP, tunnelSource, tunnelDestination):
    file = open('./ansible/variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nR1tunnelIP: {R1tunnelIP}')  # Write some text
    file.write(f'\nR2tunnelIP: {R2tunnelIP}')  # Write some text
    file.write(f'\ntunnelSource: {tunnelSource}')  # Write some text
    file.write(f'\ntunnelDestination: {tunnelDestination}')  # Write some text
    file.close()  # Close the file


if __name__ == "__main__":
    clearFile()
    Routers = ["R1", "R2", "Edge"]
    getBannerMessages(Routers[0])
    getBannerMessages(Routers[1])
    getBannerMessages(Routers[2])
    R1DHCPNetworks, R2DHCPNetworks, EdgeDHCPNetworks = [], [], []
    listOfDHCPNetworks = [R1DHCPNetworks, R2DHCPNetworks, EdgeDHCPNetworks]
    for i in range(2):
        getDetailsDHCP(listOfDHCPNetworks[i], Routers[i])
    R1Networks, R2Networks, EdgeNetworks = [], [], []
    listOfOSPFNetworks = [R1Networks, R2Networks, EdgeNetworks]
    for i in range(3):
        getOSPFdetails(listOfOSPFNetworks[i], Routers[i])
        writeNetworksToFile(listOfOSPFNetworks[i], Routers[i])
    print("We're done with the OSPF configuration let's now configure the VPN tunnel.")
    getVPNDetails()
    os.system("ansible-playbook ./ansible/main.yml -u cisco -k")
