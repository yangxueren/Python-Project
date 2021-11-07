import telnetlib
import time
import logging

class telnetServer():
    def __init__(self):
        self.tn = telnetlib.Telnet()

    def logging_host(self, host_ip, port, username, password):
        try:
            self.tn.open(host_ip, port)
        except:
            logging.warning('网络连接失败')
            return False
        self.tn.read_until(b'localhost login:: ', timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        time.sleep(3)
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        time.sleep(3)
        logging_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' in logging_result:
            logging.warning('The Username or Password is not correct.')
            return False
        else:
            logging.warning('Logged successfully.')
            return True
    def execute_command(self, command):
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(3)
        execute_result = self.tn.read_very_eager().decode('ascii')
        print(execute_result)

    def logout(self):
        self.tn.close()

if __name__ == '__main__':
    host_ip = '192.168.0.12'
    port = '23'
    username = 'yang'
    password = 'linuxprobe'
    command = 'ls'
    logtry = telnetServer()
    logtry.logging_host(host_ip, port, username, password)
    logtry.execute_command(command)
    logtry.logout()