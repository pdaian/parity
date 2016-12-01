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


chaindata = "blocknum,size,timestamp,difficulty,num_transactions,size\n"

x = 0
while 1:
    block_data_str = ""
    block_data = call_method("eth_getBlockByNumber", params = [str(hex(x)), False])['result']
    if block_data is None:
        break
    block_data_str += str(x) + ","
    block_data_str += str(int(block_data['size'],16)) + ","
    block_data_str += str(int(block_data['timestamp'],16)) + ","
    block_data_str += str(int(block_data['difficulty'],16)) + ","
    block_data_str += str(len(block_data['transactions'])) + ","
    block_data_str += str(int(block_data['size'],16))
    x += 1
    chaindata += block_data_str + "\n"


open("/home/ubuntu/chaindata", "w").write(chaindata)
print "All done!"
