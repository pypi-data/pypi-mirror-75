import requests
import json
from aimaxsdk import tool
import os
import base64
from aimaxsdk import errors


class Auth:

    def __init__(self):
        pass

    def login(self, username, password):
        pass

    def logout(self, username):
        pass

    def get_credential(self, username):
        pass

    def get_token(self, username):
        pass



folder_aimax = "{}/.aimax".format(os.path.expanduser("~"))
if os.path.isdir(folder_aimax):
    #print('dir exist')
    print('')
else:
    #print('dir not exist')
    os.mkdir(folder_aimax)

class SimpleAuth(Auth):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.folder_server = "{}/{}_{}".format(folder_aimax, self.host, self.port)
        #print(self.folder_server)

    def __int__(self, config_file):
        super().__init__()
        # TODO: load host and port config from file

    def login(self, username, password):
        url = "http://{}:{}/s/api/auth/login".format(self.host, self.port)
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps({"username": username, "password": password}), headers=headers)
        print(url)
        #print('====================11')

        #print(json.dumps({"username": username, "password": password}))
        ok, data = tool.parse_response(response, "data", "token")
        if ok:
            ok, user = tool.parse_response(response, "data", "user")
            self._save_token(data, user, username, password)
        else:
            print(data)

    # Convert a dict to json and encrypt that
    def _encode_data(self, data):
        content = json.dumps(data)
        b_content = base64.b64encode(content.encode(encoding="utf-8"))
        return b_content.decode()

    def _decode_data(self, data):
        content = base64.b64decode(data).decode(encoding="utf-8")
        return json.loads(content)

    def _save_token(self, token, user, username, password):
        if not os.path.exists(self.folder_server):
            os.makedirs(self.folder_server, 0o755)
        for key in user:
            token[key] = user[key]
        token["plain_password"] = password
        token_path = "{}/token_{}".format(self.folder_server, username)
        with open(token_path, "w") as fp:
            fp.write(self._encode_data(token))

    def logout(self, username):
        token_path = "{}/token_{}".format(self.folder_server, username)
        with open(token_path) as fp:
            content = ""
            for line in fp.readlines():
                content = content + line
            data = self._decode_data(content)
            url = "http://{}:{}/s/api/auth/logout/{}".format(self.host, self.port, data["id"])
            response = requests.get(url)
            ok, _ = tool.parse_response(response)
            if ok:
                os.remove(token_path)

    def get_credential(self, username):
        token_path = "{}/token_{}".format(self.folder_server, username)
        with open(token_path) as fp:
            content = ""
            for line in fp.readlines():
                content = content + line
            return self._decode_data(content)

    def get_token(self, username):
        credential = self.get_credential(username)
        return credential["signature"]


class Connections(object):

    def __init__(self):
        self.conns = {}

    def load(self):
        self.conns.clear()
        for file in os.listdir(folder_aimax):
            host_port = file.split("_")
            conn_key = "{}_{}".format(host_port[0], host_port[1])
            conn_auth = SimpleAuth(host_port[0], host_port[1])
            self.conns[conn_key] = conn_auth

    def connect(self, host, port, username, password):
        conn_key = "{}_{}".format(host, port)
        conn_auth = self.conns.get(conn_key)
        if conn_auth is None:
            conn_auth = SimpleAuth(host, port)
            self.conns[conn_key] = conn_auth
        conn_auth.login(username, password)

    def disconnect(self, host, port, username):
        conn_key = "{}_{}".format(host, port)
        conn_auth = self.conns.get(conn_key)
        if conn_auth is not None:
            conn_auth.logout(username)
            del self.conns[conn_key]

    def token(self, host, port, username):
        conn_key = "{}_{}".format(host, port)
        conn_auth = self.conns.get(conn_key)
        if conn_auth is not None:
            return conn_auth.get_token(username)
        else:
            raise errors.ClientException("Please login in first")

    def credential(self, host, port, username):
        conn_key = "{}_{}".format(host, port)
        conn_auth = self.conns.get(conn_key)
        if conn_auth is not None:
            return conn_auth.get_credential(username)
        else:
            raise errors.NotSignedInException("Please login in first")

    def check_password(self, host, port, username, password):
        cre = self.credential(host, port, username)
        if cre is not None:
            if password == cre["plain_password"]:
                return True
            else:
                return False
        else:
            raise errors.NotSignedInException("Please login in first")

    def list_all(self):
        return self.conns.keys()


if __name__ == "__main__":
    # connections = Connections()
    # connections.connect("192.168.124.95", "38886", "super", "P@ssw0rd")
    # print(connections.credential("192.168.124.95", "38886", "super"))
    # print(connections.check_password("192.168.124.95", "38886", "super", "P@ssw0rd"))
    file_path = os.path.abspath(__file__)
    print(file_path[0:file_path.rindex("/")])
    print(file_path.rindex("/"))
    print(os.path.abspath(__file__))
    # auth.logout()
