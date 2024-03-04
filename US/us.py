from flask import Flask, abort, request
import requests
import socket
import json

app = Flask(__name__)

def validate_run(hostname,fs_port,num,as_ip,as_port):
    if(hostname == '' or fs_port == '' or num == '' or as_ip == '' or as_port == ''):
        print(f"BAD_REQUEST : {400}")
    else:
        print(f"OK : {200}")

def fibo_Url(ip,num):
    url = f"http://{ip}:9090/fibonacci?number='{num}"
    return url

def dnsQuery(hostname):
    TYPE = "A"
    query = str(f"NAME={hostname} \n #TYPE={TYPE}")
    return query

def queryIpfromAS(hostname,as_ip,as_port):
    socket_us = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    dnsquery = dnsQuery(hostname)
    server = (as_ip,int(as_port))
    socket_us.sendto(str.encode(dnsquery),server)
    response = socket_us.recvfrom(1024)
    response = json.loads(response[0].decode())
    return response

@app.route('/fibonacci')
def index():
    hostname = request.args['hostname']
    fs_port = request.args['fs_port']
    number = request.args['number']
    as_ip = request.args['as_ip']
    as_port = request.args['as_port']
    validate_run(hostname,fs_port,number,as_ip,as_port)

querydict ={'TYPE':'A','NAME':hostname}
response = queryIpfromAS(hostname, as_ip, as_port)
print("RESPONSE from server is: ", response)

fibonacci_ip = response['VALUE']
fibonacciqueryurl = fibo_Url(fibonacci_ip, number)
result = requests.get(fibonacciqueryurl)
print (result.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080, debug=True)
