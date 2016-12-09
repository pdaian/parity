import os, time, sys

try:
    base_path = sys.argv[1].strip()
except:
    print "Usage: python automated_install.py [home directory including trailing /]"
    print "EG (AWS Ubuntu): python automated_install.py /home/ubuntu/"
    exit(1)

if base_path[-1] != '/':
   print "Invalid path.  Must contain trailing /"
   exit(1)

os.chdir(base_path)
os.system("git clone https://github.com/pdaian/parity")
os.chdir(base_path + "parity")
os.system("git checkout snowwhite")
os.system("cp -R skeleton/* " + base_path + ".")
time.sleep(5)
os.system("git pull")
time.sleep(5)
os.system("cargo build")
time.sleep(5)
os.chdir("" + base_path + "parity/target/debug")
print "STARTING DAEMON..."
os.system(base_path + "parity/target/debug/parity daemon " + base_path + 'pid --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --rpccorsdomain "http://54.198.251.130:8000" --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 25')
time.sleep(20)
os.system("python " + base_path + "parity/pyrpc/provision_credentials.py")
print "WROTE CONFIG, PROVISIONED CREDENTIALS"
time.sleep(10)
os.system("killall -9 parity")
print "KILLED DAEMON. RESTARTING WITH NEW CREDENTIALS...."
time.sleep(10)
print "STARTING SNOWWHITE"
os.system(base_path + "parity/target/debug/parity daemon " + base_path + 'pid --jsonrpc-apis "parity_set,parity,eth,parity_accounts,personal" -l info --rpccorsdomain "http://54.198.251.130:8000" --jsonrpc-interface all --jsonrpc-hosts="all" --max-peers 25 --bootnodes enode://abbf1b75458931295d7b9e84aada2d7dc3cd9bb446019cfaa978d148a44d5ab51133c8bcc8175087c5b27dc0d3bbc53aff5089784934e00b48e1eb347818e537@172.31.13.94:30303')
print "ALL DONE!"
