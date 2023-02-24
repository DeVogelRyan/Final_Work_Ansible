import re
import os


def clearFile():
    if not os.path.exists("ansible"):
        os.makedirs("ansible")
    file = open('./ansible/variables.yml', 'a')  # Open a file in append mode
    file.truncate(0)  # Clear all the text
    file.close()  # Close the file for safety reasons


def valid_ip_address(ip_address):
    # This means that a given IP address must follow this example: 192.168.1.0
    match = re.match(
        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip_address)
    # return True if it matches (so it's a valid ip address) or False if it doesn't
    return bool(match)


def checkInputDHCP(network, subnet):
    # Check if the ip address and the wildcard look like an ip addresses.
    # Also check if the area is a normal number/integer so no 0.5...
    if valid_ip_address(network) == False or valid_ip_address(subnet) == False:
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
