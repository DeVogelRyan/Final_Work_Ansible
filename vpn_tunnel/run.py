import os

#os.system("ansible-playbook main.yml -u cisco -k")


R1tunnelIP = input("[R1] Tunnel ip address: ")
tunnelSource = input("[R1] Tunnel source: ")
tunnelDestination = input("[R1] Tunnel destination: ")
R2tunnelIP = input("[R2] Tunnel ip address: ")

file = open('variables.yml', 'a') # Open a file in append mode
file.write(f'\nR1tunnelIP: {R1tunnelIP}') # Write some text
file.write(f'\ntunnelSource: {tunnelSource}') # Write some text
file.write(f'\ntunnelDestination: {tunnelDestination}') # Write some text
file.write(f'\nR2tunnelIP: {R2tunnelIP}') # Write some text
file.close() # Close the file
