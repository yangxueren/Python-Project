import paramiko
import time
import logging

ip = "192.168.0.12"
username = 'yang'
password = 'linuxprobe'
sshct = paramiko.SSHClient()
sshct.set_missing_host_key_policy(paramiko.AutoAddPolicy)
sshct.connect(hostname=ip, username=username, password=password)
command = sshct.invoke_shell()
command.send("dis cur\n")
time.sleep(3)
output = command.recv(65535)
print(output.decode('ascii'))




