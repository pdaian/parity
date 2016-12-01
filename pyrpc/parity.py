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

# Get miner address
miner_id = int(requests.get("http://54.198.251.130:5000/get_my_ip").text.strip())
method_result = call_method("parity_newAccountFromPhrase", [str(miner_id), "test"])
print method_result
addr = str(method_result['result'])
params = [{
			"from": addr,
                        "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
                        "gas": "0x76c0",
                        "gasPrice": "0x9184e72a000",
                        "value": "0x9184e72a"
                }]

while 1:
    print call_method("eth_blockNumber")
    print call_method("eth_sendTransaction", params)




















    #time.sleep(30)
print call_method("parity_enode")
print call_method("parity_addReservedPeer", ["enode://1da9a307ae469ee2c3a7d38c79fb290c8b815af71ca3d434cb27ecff4421caddfd1df55969313dea284975341027a21bde655b8a1a398e357b894d2a0c60f5f3@162.248.4.26:30303"])
exit(1)
print tx
print call_method("eth_getTransactionReceipt", [str(tx['result'])])
for i in range(0, 100):
    addr = str(call_method("parity_newAccountFromPhrase", [str(i), ""])['result'])
    open("/home/ubuntu/addrs", "a").write(addr + "\n")
exit(1)
