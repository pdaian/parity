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

while 1:
    call_method("eth_sendTransaction", params)
    print call_method("eth_blockNumber")
    #time.sleep(30)
print call_method("parity_enode")
print call_method("parity_addReservedPeer", ["enode://1da9a307ae469ee2c3a7d38c79fb290c8b815af71ca3d434cb27ecff4421caddfd1df55969313dea284975341027a21bde655b8a1a398e357b894d2a0c60f5f3@162.248.4.26:30303"])
exit(1)
print tx
print call_method("eth_getTransactionReceipt", [str(tx['result'])])
