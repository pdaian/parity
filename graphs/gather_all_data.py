import os

nodes = open("/home/ubuntu/nodes").read().splitlines()
for node_id in range(0, len(nodes)):
    node = nodes[node_id]
    basedir = "/home/ubuntu/data/" + str(node_id)
    os.system("mkdir " + basedir)
    os.system("scp -i phil-bitcoin.pem ubuntu@" + node.strip() + ":chaindata " + basedir + "/.")
    os.system("scp -i phil-bitcoin.pem ubuntu@" + node.strip() + ":landmarks " + basedir + "/.")
    os.system("scp -i phil-bitcoin.pem ubuntu@" + node.strip() + ":resources " + basedir + "/.")
