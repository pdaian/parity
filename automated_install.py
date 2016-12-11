import os, time, sys, subprocess as sp, json

try:
    base_path = sys.argv[1].strip()
    remote_ip = sys.argv[2].strip()
    bootstrap = sys.argv[3].strip()
except:
    print "Usage: python automated_install.py [home directory including trailing /] [key distribution server IP] [bootsrap enode]"
    print "EG (AWS Ubuntu): python automated_install.py /home/ubuntu/ 0.0.0.0 enode://..."
    exit(1)

if base_path[-1] != '/':
   print "Invalid path.  Must contain trailing /"
   exit(1)

os.system("sudo apt-get update --fix-missing")
os.system("sudo apt-get install -y git make build-essential g++")
os.system("curl https://sh.rustup.rs -sSf | sh -s -- -y")
os.chdir(base_path)
os.system("git clone https://github.com/pdaian/parity")
os.chdir(base_path + "parity")
os.system("git checkout snowwhite")
os.system("git pull")
os.chdir(base_path + "parity/skeleton")
os.system("cp -a . " + base_path)
os.system(base_path + ".cargo/bin/cargo build --release")
os.chdir("" + base_path + "parity/target/release")
time.sleep(5)
print "\n"
print "STARTING DAEMON..."
os.system(base_path + "parity/target/release/parity daemon " + base_path + 'pid --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 25')
time.sleep(20)
os.system("python " + base_path + "parity/pyrpc/provision_credentials.py " + base_path + " " + remote_ip)
print "WROTE CONFIG, PROVISIONED CREDENTIALS"
time.sleep(10)
os.system("killall -9 parity")
print "KILLED DAEMON. RESTARTING WITH NEW CREDENTIALS...."
time.sleep(10)
print "STARTING SNOWWHITE"
os.system(base_path + "parity/target/release/parity daemon " + base_path + 'pid --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 25 --bootnodes ' + bootstrap)
print "ALL DONE!"
