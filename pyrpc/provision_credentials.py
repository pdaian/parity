import requests, json, time, sys

def call_method(method, params=[]):
	payload = {
		"jsonrpc":"2.0",
	        "method": method,
        	"params": params,
	        "id": 83,
	}
	return do_request(payload)

def do_request(payload):
    url = "http://localhost:8545/"
    headers = {'content-type': 'application/json'}

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response


params = [{
			"from": "0xbfbd48cb48c61db8a69724f60239bf7c9cbab986",
                        "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
                        "gas": "0x76c0",
                        "gasPrice": "0x9184e72a000",
                        "value": "0x9184e72a"
                }]


config_text = """[parity]
chain = "[2]chain_spec.json"

[account]
unlock = ["[1]"]
password = ["[2]accountpassword"]

[mining]
author = "[1]"
reseal_on_txs = "all"
force_sealing = false
"""

try:
    sys.argv[1]
    sys.argv[2]
except:
    print "Usage: python provision_credentials.py [home directory including trailing /] [credential server IP]"
    print "EG (AWS Ubuntu): python provision_credentials.py /home/ubuntu/ 0.0.0.0"
    exit(1)


# Get miner address
miner_id = int(requests.get("http://" + sys.argv[2].strip() + ":5000/get_my_ip").text.strip())
method_result = call_method("parity_newAccountFromPhrase", [str(miner_id), "test"])
print method_result
addr = str(method_result['result'])
open(sys.argv[1] + '.parity/address', 'w').write(addr)

print "got addr", addr

config_text = config_text.replace("[1]", addr)
config_text = config_text.replace("[2]", sys.argv[1])
open('/home/ubuntu/.parity/config.toml', 'w').write(config_text)
print "Wrote config.  Ready to mine!"
