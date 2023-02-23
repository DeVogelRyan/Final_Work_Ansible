import os
from network import OSPF
# os.system("ansible-playbook main.yml -u cisco -k")
import re


def clearFile():
    file = open('variables.yml', 'a')  # Open a file in append mode
    file.truncate(0)  # Clear all the text
    file.close()  # Close the file for safety reasons


def valid_ip_address(ip_address):
    # This means that a given IP address must follow this example: 192.168.1.0
    match = re.match(
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address)
    # return True if it matches (so it's a valid ip address) or False if it doesn't
    return bool(match)


def checkInputOSPF(ip, wildcard, area):
    # Check if the ip address and the wildcard look like an ip addresses.
    # Also check if the area is a normal number/integer so no 0.5...
    if valid_ip_address(ip) == False or valid_ip_address(wildcard) == False or not area.isnumeric():
        print("One of the inputs was wrong let's start again.")
        return False


def checkIP(ip):
    # Check if the ip address look like an ip addresses.
    if valid_ip_address(ip) == False:
        print("One of the inputs was wrong let's start again.")
        return False


# This is a basic menu we keep repeating to ask if a user would like to create a new network.
def Menu(question):
    # First the inputis converted to a string and also lower it so 'Y becomes y' for example and also strip any spaces.
    answer = str(input(question+' (y/n): ')).lower().strip()
    if answer[:1] == 'y':
        return True
    elif answer[:1] == 'n':
        return False
    else:
        print("Invalid input! ")
        Menu(question)


def getOSPFdetails(OSPFList: list, TAG: str):
    print("setup a network for OSPF...")
    ip = input(f"[{TAG}] IP address: ")
    wildcard = input(f"[{TAG}] Wildcard mask: ")
    area = input(f"[{TAG}] Area: ")
    # Checking if all the details are valid. Else we ask to fill it in again.
    if checkInputOSPF(ip, wildcard, area) == False:
        getOSPFdetails(OSPFList, TAG)
        return
    # adding our class to a list
    OSPFList.append(OSPF(TAG, ip, wildcard, area))
    if Menu(f"Do you want to configure another network for {TAG}") == True:
        getOSPFdetails(OSPFList, TAG)
        return


def writeNetworksToFile(OSPFList: list, TAG: str):
    file = open('variables.yml', 'a')  # Open a file in append mode
    file.write(f'\n{TAG}network:')  # Write some text
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
    R1Networks, R2Networks, EdgeNetworks = [], [], []
    listOfNetworks = [R1Networks, R2Networks, EdgeNetworks]
    Routers = ["R1", "R2", "Edge"]
    for i in range(3):
        getOSPFdetails(listOfNetworks[i], Routers[i])
        writeNetworksToFile(listOfNetworks[i], Routers[i])
    print("We're done with the OSPF configuration let's now configure the VPN tunnel.")
    getVPNDetails()
