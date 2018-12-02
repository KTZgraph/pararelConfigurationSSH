#coding=utf-8

import threading
import paramiko
import subprocess

"""
GLOBAL parameters
"""

remote_login = "user"
remote_password = "centos"
remote_host_ip = "192.168.0.12"

def one_command(remote_host_ip, remote_login, remote_password, command):
    """
    Login via user, and passwd without SSH Keys [!]
    Note:
        For security always use SSH KEYS !
    """
    client_ssh = paramiko.SSHClient()
    # client_ssh.load_host_keys('path for keys')
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # for logging via user&passwd
    client_ssh.connect(remote_host_ip, username=remote_login, password=remote_password)
    ssh_session = client_ssh.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        remote_output = ssh_session.recv(1024)
        return remote_output
    else:
        return {'code' : 3, 'message': "Can't connect to host: {host_ip}".format(host_ip = remote_host_ip)}

output = one_command(remote_host_ip, remote_login, remote_password, 'ls -la')
print(output)