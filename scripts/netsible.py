#!/usr/bin/env python

from netlib.netlib.user_creds import simple_yaml
from netlib.netlib.conn_type import SSH

from os.path import expanduser
import sys

creds = simple_yaml()
base_dir = expanduser("~/netsible")
hostname = sys.argv[1]
command_file = sys.argv[2]
ssh = SSH(hostname, creds['username'], creds['password'])

ssh.connect()
ssh.set_enable(creds['enable'])

with open(base_dir + "/" + command_file) as f:
    for line in f.readlines():
        line = line.strip()
        ssh.command(line)
f.close()

ssh.close()
