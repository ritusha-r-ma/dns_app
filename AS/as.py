from flask import abort
import socket
import json


UDP_IP = "172.18.0.2"
UDP_PORT = 53533

FILE = "register_info.json"
socket_as = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_as.bind((UDP_IP, UDP_PORT))

def getDictionary(input_data):
    list_1 = {}
    data = input_data.split("\n")
    for element in data:
        key = element.split("=")[0]
        value_1 = element.split("=")[1]
        list_1[key] = value_1
    return list_1


def update_entry(data):
    try:
        with open(FILE) as file:
            register_data = json.load(file)
    except:
        print("File not found")
        register_data = {}

    if (str(data['NAME']) in register_data):
        register_data[str(data['NAME'])]["TYPE"] = str(data['TYPE'])
        register_data[str(data['NAME'])]["VALUE"] = str(data['VALUE'])
        register_data[str(data['NAME'])]["TTL"] = int(data['TTL'])
    else:
        temp = {}
        temp["TYPE"] = str(data['TYPE'])
        temp["VALUE"] = str(data['VALUE'])
        temp["TTL"] = int(data['TTL'])
        register_data[str(data['NAME'])] = temp

    print("DATA: ", register_data)
    try:
        with open(FILE, "w+") as file:
            json.dump(register_data, file)
        print("registered")
    except:
        print("Error while registering hostname.")


def resultQuery(data):
    try:
        with open(FILE) as file:
            entry = json.load(file)
    except:
        print("Unable to open files")
        abort(400)

    hostname = ""
    query = data.split("\n")
    for q in query:
        key = q.split("=")[0]
        if (key == "NAME"):
            hostname = q.split("=")[1]
            break
    if (hostname in entry):
        response = {}
        response['NAME'] = hostname
        response['TYPE'] = entry[hostname]['TYPE']
        response['VALUE'] = entry[hostname]['VALUE']
        response['TTL'] = entry[hostname]['TTL']
        return response
    else:
        print("hostname not found in registry.")
        return {}


while True:
    print("Listening:", UDP_IP, UDP_PORT)
    data, addr = socket_as.recvfrom(1024)  # buffer size is 1024 bytes
    print("received message:", data)
    data = data.decode('utf-8')
    if (data[0] == '#'):
        print("DNS QUERY : ")
        result = resultQuery(data[1:])
        print("RESULT : ", result)
        socket_as.sendto(json.dumps(result).encode(), addr)
    else:
        dataDict = getDictionary(data)
        update_entry(dataDict)
        print("Entry created/updated")
        socket_as.sendto(str.encode("success:201"), addr)
