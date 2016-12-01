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


for i in range(0, 100):
    x = call_method("parity_newAccountFromPhrase", [str(i), "test"])
    print x
    open("/home/ubuntu/addrs", "a").write(str(x['result']) + '\n')
