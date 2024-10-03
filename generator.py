# coding=utf-8

import json


def generator():
    serverAddr = "server.corneliamo.cn"
    serverPort = 10000

    with open("frp.json", mode='r') as fp:
        frp_list = json.load(fp)

    with open("frpc.toml", mode='w') as fp:
        fp.write(f"""serverAddr = \"{serverAddr}\"
serverPort = {serverPort}
webServer.addr = \"127.0.0.1\"
webServer.port = 7400
webServer.user = \"admin\"
webServer.password = \"admin\"\n\n""")
        for item in frp_list:
            fp.write("[[proxies]]\n")
            fp.write(f"name = \"{item['name']}\"\n")
            fp.write(f"type = \"{item['type']}\"\n")
            fp.write(f"localIP = \"{item['localIP']}\"\n")
            fp.write(f"localPort = {item['localPort']}\n")
            fp.write(f"remotePort = {item['remotePort']}\n\n")
