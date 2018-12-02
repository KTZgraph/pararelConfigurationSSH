#coding=utf-8

import threading
import paramiko
import subprocess
from concurrent import futures
"""
GLOBAL parameters
"""

MAX_WORKERS = 20

host_1 = {
    "login" : "user",
    "password" : "centos",
    "ip" : "192.168.0.13",
    "file" : "command_1.txt"

}

host_2 = {
    "login" : "user2",
    "password" : "centos2",
    "ip" : "192.168.0.12",
    "file" : "command_2.txt"

}

all_hosts_list = [host_1, host_2]

def connect_via_ssh(host_data, command_list=None):
    """
    Return ssh session
    """
    client_ssh = paramiko.SSHClient()
    # client_ssh.load_host_keys('path for keys')
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # for logging via user&passwd
    client_ssh.connect(host_data["ip"], username=host_data["login"], password=host_data["password"])
    if "file" in host_data:
        with open(host_data["file"], 'r') as f:
            command_list = f.read()
        command_list = [str(i) for i in command_list.split('\n')]
        for command in command_list:
            ssh_session = client_ssh.get_transport().open_session()
            if ssh_session.active:
                ssh_session.exec_command(command)
                remote_output = ssh_session.recv(1024)
                if not remote_output:
                    print("[!]Commnad: '{command}' not found".format(command=command))
                else:
                    print("[{host}]$ {output}".format(output=remote_output, host=host_data["ip"]))
            else:
                raise ConnectionError("Can't connect to host: {address} ".format(address = host_data["ip"]))
                client_ssh.close()
    client_ssh.close()
    return {'code': 1}

def pararel_connection():
    """
    True pararell executors
    """
    workers = min(MAX_WORKERS, len(all_hosts_list))
    with futures.ThreadPoolExecutor(workers) as exectutor:
        res = exectutor.map(connect_via_ssh, all_hosts_list)
    return len(list(res))


def main():
    pararel_connection()

if __name__ == "__main__":
    main()
