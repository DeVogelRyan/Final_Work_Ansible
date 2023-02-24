import os
from network import Network
from basic_functions import *
# os.system("ansible-playbook main.yml -u cisco -k")


def getDetailsDHCP(DHCPList: list, TAG: str):
    print("setup DHCP...")
    pool = input(f"[{TAG}] Pool name: ").strip()
    defaultRouter = input(f"[{TAG}] Default-router: ")
    if (valid_ip_address(defaultRouter) == False or len(pool) == 0):
        print("One of the inputs was wrong let's start again.")
        getDetailsDHCP(DHCPList, TAG)
        return
    WriteDHCPToFile(pool, defaultRouter, TAG)
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
    if Menu(f"Do you want to configure another DHCP network for {TAG}") == True:
        getDHCPNetworks(DHCPList, TAG)
        return
    WriteDHCPListToFile(DHCPList, TAG)


def WriteDHCPToFile(pool: str, defaultRouter: str,  TAG: str):
    file = open('variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nDHCP_Pool_{TAG}: {pool}')  # Write some text
    file.write(f'\nDHCP_Default_Router_{TAG}: {defaultRouter}')
    file.close()  # Close the file


def WriteDHCPListToFile(DHCPList: list, TAG: str):
    file = open('variables.yml', 'a')  # Open a file in append mode
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
        file.write(f'\n    wildcardMask: {item.subnet}')
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
    file = open('variables.yml', 'a')  # Open a file in append mode
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
        file.write(f'\n    ip: {item.ip}')
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
    file = open('variables.yml', 'a')  # Open a file in append mode
    file.write(f'\nR1tunnelIP: {R1tunnelIP}')  # Write some text
    file.write(f'\nR2tunnelIP: {R2tunnelIP}')  # Write some text
    file.write(f'\ntunnelSource: {tunnelSource}')  # Write some text
    file.write(f'\ntunnelDestination: {tunnelDestination}')  # Write some text
    file.close()  # Close the file


if __name__ == "__main__":
    clearFile()
    R1DHCPNetworks, R2DHCPNetworks = [], []
    getDetailsDHCP(R1DHCPNetworks, "R1")
    getDetailsDHCP(R2DHCPNetworks, "R2")
    R1Networks, R2Networks, EdgeNetworks = [], [], []
    listOfNetworks = [R1Networks, R2Networks, EdgeNetworks]
    Routers = ["R1", "R2", "Edge"]
    for i in range(3):
        getOSPFdetails(listOfNetworks[i], Routers[i])
        writeNetworksToFile(listOfNetworks[i], Routers[i])
    print("We're done with the OSPF configuration let's now configure the VPN tunnel.")
    getVPNDetails()
