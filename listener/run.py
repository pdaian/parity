from flask import request, jsonify, Flask
app = Flask(__name__)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr
    nodes = open('/home/ubuntu/nodes', 'r').read()
    # Give em a fresh address
    id = int(open('/home/ubuntu/counter').read().strip())
    open('/home/ubuntu/counter', 'w').write(str(id + 1))
    # Track IP
    if not ip in nodes:
        open('/home/ubuntu/nodes', 'a').write(ip + '\n')
    return str(id % 100)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
