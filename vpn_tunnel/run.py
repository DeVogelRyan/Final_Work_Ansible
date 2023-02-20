import os
from network import OSPF
# os.system("ansible-playbook main.yml -u cisco -k")
import re


def valid_ip_address(ip_address):
    match = re.match(
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address)
    return bool(match)


def checkInput(ip, wildcard, area):
    if (valid_ip_address(ip) == False):
        print("Ip address was wrongly formatted!")
    elif (valid_ip_address(wildcard) == False):
        print("Wildcard was wrongly formatted!")
    elif (not area.isnumeric()):
        print("Wildcard was wrongly formatted!")


def getOSPFNetworks(OSPFList: list, TAG: str):
    while True:
        print("setup a network for OSPF...")
        print("Leave any number blank to stop.")
        ip = input(f"[{TAG}] IP address: ")
        wildcard = input(f"[{TAG}] Wildcard mask: ")
        area = input(f"[{TAG}] Area: ")
        checkInput(ip, wildcard, area)
        if ip == "" or wildcard == "" or area == "":
            break
        OSPFList.append(OSPF(TAG, ip, wildcard, area))


R1Networks = []
R2Networks = []
# getOSPFNetworks(R1Networks, "R1")
# getOSPFNetworks(R2Networks, "R2")



"""
file = open('variables.yml', 'a')  # Open a file in append mode
file.write(f'\nOSPF:')  # Write some text
file.write(f'\n  network{newClass.id}:')  # Write some text
file.write(f'\n    ip: {newClass.ip}')  # Write some text
file.write(f'\n    wildcardMask: {newClass.wildcard}')  # Write some text
file.write(f'\n    area: {newClass.area}')  # Write some text
file.write(f'\n  network{newClass.id}:')  # Write some text
file.write(f'\n    ip: {newClass.ip}')  # Write some text
file.write(f'\n    wildcardMask: {newClass.wildcard}')  # Write some text
file.write(f'\n    area: {newClass.area}')  # Write some text
file.close()  # Close the file """

"""
tunnelSource = input("[R1] Tunnel source: ")
tunnelDestination = input("[R1] Tunnel destination: ")
R2tunnelIP = input("[R2] Tunnel ip address: ")

file = open('variables.yml', 'a')  # Open a file in append mode
file.write(f'\nR1tunnelIP: {R1tunnelIP}')  # Write some text
file.write(f'\ntunnelSource: {tunnelSource}')  # Write some text
file.write(f'\ntunnelDestination: {tunnelDestination}')  # Write some text
file.write(f'\nR2tunnelIP: {R2tunnelIP}')  # Write some text
file.close()  # Close the file """
