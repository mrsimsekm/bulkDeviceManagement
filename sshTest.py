import paramiko
import time
from datetime import date, timedelta, datetime

host_file = open("hosts.txt", "r")
hosts = host_file.read().split('\n')
host_file.close()

credentials_file = open("credentials.txt", "r")
credentials = credentials_file.read().split('\n')
credentials_file.close()
username = credentials[0]
password = credentials[1]

#username = 'tpcadmin'
#password = 'Tpc@dm1n'
output_text = ""

command_file = open("commands.txt", "r")
commands = command_file.read().split('\n')
command_file.close()

session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for host in hosts:
    try:
        print(f"\n{'#'*50}\nConnecting to the Device {host} \n{'#'*50}\n")
        output_text += (f"\n{'#'*50}\nConnecting to the Device {host} \n{'#'*50}\n")
        session.connect(hostname=host,
                        username=username,
                        password=password,
                        )
        DEVICE_ACCESS = session.invoke_shell()
        for command in commands:
            DEVICE_ACCESS.send(f'{command}\n')
            time.sleep(.5)
            output = DEVICE_ACCESS.recv(65000)
            print (output.decode(), end='')
            output_text += str(output.decode())
        session.close()
    except:
        print("Unable to connect to the Device")
        output_text += "Unable to connect to the Device"

output_file_name = time.strftime("%Y%m%d-%H%M%S")
output_file = open(output_file_name, "w")
output_file.write(output_text)
output_file.close()