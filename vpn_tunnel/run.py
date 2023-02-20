import os
from network import OSPF
# os.system("ansible-playbook main.yml -u cisco -k")

newClass = OSPF("R1", "192.168.1.0", "0.0.0.255", 0)
newClass.func()

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
