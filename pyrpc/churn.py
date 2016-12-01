import time

DOWNTIME = 60
COOLOFF = 60
NUM_NODES = 20

import os
from random import sample
allnodes = open("/home/ubuntu/nodes").read().splitlines()
allnodes = [x.strip() for x in allnodes]

def do_cmd(command, node, append=''):
    cmd = "ssh -o StrictHostKeyChecking=no -i phil-bitcoin.pem ubuntu@" + node + ' -t "' + command + '"' + append
    print cmd
    os.system(cmd)

while 1:
    nodes = sample(allnodes, NUM_NODES)
    for node in nodes:
        do_cmd("killall -9 parity &", node, ' &')
    time.sleep(DOWNTIME)
    for node in nodes:
        do_cmd('''/home/ubuntu/parity/target/release/parity daemon /home/ubuntu/pid --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 200 --nat=upnp''', node)
    time.sleep(10)
    for node in nodes:
        do_cmd('''nohup python /home/ubuntu/parity/pyrpc/parity.py </dev/null > /dev/null 2>&1 &''', node)
    time.sleep(COOLOFF)
