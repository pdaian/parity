import requests, json, time

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
chain = "/home/ubuntu/chain_spec.json"

[account]
unlock = ["[1]"]
password = ["/home/ubuntu/accountpassword"]

[mining]
author = "[1]"
reseal_on_txs = "none"
force_sealing = true
"""


# Get miner address
miner_id = int(requests.get("http://54.198.251.130:5000/get_my_ip").text.strip())
method_result = call_method("parity_newAccountFromPhrase", [str(miner_id), "test"])
print method_result
addr = str(method_result['result'])

print "got addr", addr

config_text = config_text.replace("[1]", addr)
open('/home/ubuntu/.parity/config.toml', 'w').write(config_text)
print "Wrote config.  Ready to mine!"
