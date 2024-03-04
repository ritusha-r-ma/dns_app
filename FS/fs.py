from flask import Flask, abort, request
import requests
import socket
import json

app = Flask(__name__)

@app.route('/fibonacci')
def fiboseries(n):
    fibo = [1, 1]
    for i in range(2, n):
        fibo.append(fibo[i-1] + fibo[i-2])
    return str(fibo)

requestdict = { "hostname" : " ",
            "ip" : " ",
            "as_ip" : " ",
            "as_port" : " " }

@app.route('/register', methods= ["PUT","GET"])
def register():
    if requests.method == "GET" or requests.method == "PUT":
        try:
            received_input = request.data
            input_string = json.load(received_input.decode('utf-8'))
            requestdict["hostname"]= str(input_string["hostname"])
            requestdict["ip"] = str(input_string["ip"])
            requestdict["as_ip"] = str(input_string["as_ip"])
            requestdict["as_port"] = str(input_string["as_port"])
            print(requestdict)
        except:
            abort(400)
    else:
        response = registerFSonAS()
        print(response)

def registerFSonAS():
    as_ip = requestdict["as_ip"]
    as_port = requestdict["as_port"]
    server_address=(as_ip,str(as_port))
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((as_ip, as_port))
    server.listen()
    conn, addr = server.accept()
    print(f"connection accepted from: {addr}")
    while 1:
        message = generatedmessage()
        socketfs.sendto(str.encode(message),server_address)
        responsefromserver = socketfs.recvfrom(1024)
        print(responsefromserver)

def generatedmessage():
    message = f"TYPE=A\n NAME= {requestdict['hostname']} \n VALUE= {requestdict['ip']} \n TTL=10"
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 9090, debug=True)
