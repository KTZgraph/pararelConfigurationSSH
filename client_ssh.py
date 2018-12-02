#coding=utf-8

import threading
import paramiko
import subprocess
from concurrent import futures
"""
GLOBAL parameters
"""

host_1 = {
    "login" : "user",
    "password" : "centos",
    "ip" : "192.168.0.12",
    "file" : "command_1.txt"

}

host_2 = {
    "login" : "user2",
    "password" : "centos2",
    "ip" : "192.168.0.33",
    "file" : "command_2.txt"

}


def connect_via_ssh(host_data, command_list=None):
    """
    Return ssh session
    """
    client_ssh = paramiko.SSHClient()
    # client_ssh.load_host_keys('path for keys')
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # for logging via user&passwd
    client_ssh.connect(host_data["ip"], username=host_data["login"], password=host_data["password"])
    ssh_session = client_ssh.get_transport().open_session()
    if ssh_session.active:
        if "file" in host_data:
            with open(host_data["file"], 'r') as f:
                command_list = f.read()
            command_list = [str(i) for i in command_list.split('\n')]
            for command in command_list:
                ssh_session.exec_command(command)
                remote_output = ssh_session.recv(1024)
                print(remote_output)
        return ssh_session
    else:
        raise ConnectionError("Can't connect to host: {address} ".format(address = host_data["ip"]))



def main():
    ssh_session_1 = connect_via_ssh(host_1)
    ssh_session_2 = connect_via_ssh(host_2)

if __name__ == "__main__":
    main()
