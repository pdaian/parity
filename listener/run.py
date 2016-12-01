from flask import request, jsonify, Flask
app = Flask(__name__)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    ip = request.remote_addr
    nodes = open('/home/ubuntu/nodes', 'r').read()
    id = int(open('/home/ubuntu/counter').read().strip())
    if not ip in nodes:
        open('/home/ubuntu/nodes', 'a').write(ip + '\n')
        open('/home/ubuntu/counter', 'w').write(str(id + 1))
    return str(id % 100)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
