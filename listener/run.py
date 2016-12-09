from flask import request, jsonify, Flask
import sys, os
app = Flask(__name__)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr
    nodes = open(sys.argv[1] + 'nodes', 'r').read()
    # Give em a fresh address
    id = int(open(sys.argv[1] + 'counter').read().strip())
    open(sys.argv[1] + 'counter', 'w').write(str(id + 1))
    # Track IP
    if not ip in nodes:
        open(sys.argv[1] + 'nodes', 'a').write(ip + '\n')
    return str(id % 100)

if __name__ == '__main__':
    path = sys.argv[1]
    os.system("touch " + path + "nodes")
    open(path + "counter", "w").write("1")
    app.run(host='0.0.0.0')
