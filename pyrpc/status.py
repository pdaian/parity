import requests, json, time

def call_method(method, params=[], url="http://localhost:8545/"):
	payload = {
		"jsonrpc":"2.0",
	        "method": method,
        	"params": params,
	        "id": 83,
	}
	return do_request(payload, url)

def do_request(payload, url):
    headers = {'content-type': 'application/json'}

    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    return response





while 1:
    output = ""
    print "\n" * 100
    for node in open('/home/ubuntu/nodes').read().strip().splitlines():
        try:
            enode = str(call_method("parity_enode", url="http://" + node.strip() + ":8545/")['result'])
            blocknum = str(call_method("eth_blockNumber")['result'])
            output += node + " @# " + str(blocknum) +  " ENode: " + enode + "\n"
        except:
            print node, "DEAD"
    print output.strip()
    time.sleep(5)
