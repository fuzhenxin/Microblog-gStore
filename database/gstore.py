import requests

defaultServerIP = "127.0.0.1"


class GstoreConnector:
    def __init__(self, ip, port, username, password):
        if ip == "localhost":
            self.serverIP = defaultServerIP
        else:
            self.serverIP = ip
        self.serverPort = port
        self.username = username
        self.password = password
        self.Url = "http://{}:{}".format(self.serverIP, self.serverPort)

    def url_encode(self, s):
        ret = ""
        for i in range(len(s)):
            c = s[i]
            if ord(c) in [42, 45, 46, 47, 58, 95]:
                ret += c
            elif (ord(c) >= 48) and (ord(c) <= 57):
                ret += c
            elif (ord(c) >= 65) and (ord(c) <= 90):
                ret += c
            elif (ord(c) >= 97) and (ord(c) <= 122):
                ret += c
            elif ord(c) >= 256:
                ret += chr(ord(c))
            elif (ord(c) != 9) and (ord(c) != 10) and (ord(c) != 13):
                ret += "{}{:X}".format("%", ord(c))
        return ret

    def get(self, strUrl):
        r = requests.get(self.url_encode(strUrl))
        return r.json()

    def fGet(self, strUrl, filename):
        r = requests.get(self.url_encode(strUrl), stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(4096):
                fd.write(chunk)
        return

    def load(self, db_name, username, password):
        cmd = self.Url + "/?operation=load&db_name=" + db_name + "&username=" + username + "&password=" + password
        res = self.get(cmd)
        print(res)
        if res == "load database done.":
            return True
        return False

    def unload(self, db_name, username, password):
        cmd = self.Url + "/?operation=unload&db_name=" + db_name + "&username=" + username + "&password=" + password
        res = self.get(cmd)
        print(res)
        if res == "unload database done.":
            return True
        return False

    def build(self, db_name, rdf_file_path, username, password):
        cmd = self.Url + "/?operation=build&db_name=" + db_name + "&ds_path=" + rdf_file_path + "&username=" + username + "&password=" + password
        res = self.get(cmd)
        print(res)
        if res == "import RDF file to database done.":
            return True
        return False

    def query(self, db_name, sparql):
        cmd = self.Url + "/?operation=query&username=" + self.username + "&password=" + self.password + "&db_name=" + db_name + "&format=json&sparql=" + sparql
        return self.get(cmd)

    def fquery(self, username, password, db_name, sparql, filename):
        cmd = self.Url + "/?operation=query&username=" + username + "&password=" + password + "&db_name=" + db_name + "&format=json&sparql=" + sparql
        self.fGet(cmd, filename)
        return

    def show(self):
        cmd = self.Url + "/?operation=show"
        return self.get(cmd)

    def user(self, type, username1, password1, username2, addition):
        cmd = self.Url + "/?operation=user&type=" + type + "&username1=" + username1 + "&password1=" + password1 + "&username2=" + username2 + "&addition=" + addition
        return self.get(cmd)

    def showUser(self):
        cmd = self.Url + "/?operation=showUser"
        return self.get(cmd)


if __name__ == '__main__':
    gc = GstoreConnector('127.0.0.1', 2567, 'root', '123456')
    """sparql = ''' prefix sound: <http://www.unisound.com/knowledge_graph/vocab/>
        select ?song where{
         ?song sound:song_composer "".
        }
    '''
    """
    # sparql = 'select ?m where {?m <file:///D:/d2rq-0.8.1/vocab/weibo_uid> "2452144190".}'
    sparql = '''prefix wb: <file:///D:/d2rq-0.8.1/vocab/>
                    delete { ?user wb:user_password ?p}
                    insert { ?user wb:user_password "268384304"}
                    where { ?user wb:user_uid "2683843043". ?user wb:user_password ?p } 
                   '''
    print(sparql)
    response = gc.query('weibo', sparql)
    print(response['StatusMsg'])
    print(response)
    print(response['results'])
