import requests, json, time, random

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
        url, data=json.dumps(payload), headers=headers, timeout=3.0).json()

    return response



enodes = []

for node in open('/home/ubuntu/nodes').read().strip().splitlines():
    try:
        enode = str(call_method("parity_enode", url="http://" + node.strip() + ":8545/")['result']).split("@")[0] + "@" + node.strip() + ":30303"
        enodes.append(enode)
    except:
        pass

nodelist = open('/home/ubuntu/nodes').read().strip().splitlines()
random.shuffle(nodelist)
for node in nodelist:
    try:
        for enode in enodes:
            print call_method("parity_addReservedPeer", params=[enode], url="http://" + node.strip() + ":8545/"), node, enode
    except:
        pass
    
    time.sleep(5)
