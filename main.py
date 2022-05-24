import typing, webbrowser, io, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
class AuthServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path).query
        pairs = parsed.split('&')
       
        code = pairs[0].split('=')[1]
        with open("/tmp/pyspot/code.txt", 'w') as f:
            f.write(code)

        self.send_response(200)
        self.send_header("Content-Type", "text/html");
        self.end_headers()
        
        fp = str(os.path.realpath(__file__)).split('/')
        fp.pop()
        okF = '/'.join(fp)
        with open(okF+"/assets/ok.html", 'r') as f:
            self.wfile.write(bytes(f.read(), 'utf-8'))
  
def doAuthFlow(port: int, url: str):
    ws = HTTPServer(("localhost", port), AuthServer)
    ws.socket.settimeout(15)
    webbrowser.open_new_tab(url)
    ws.handle_request()
    
import socket, json#,xml TODO
class Config:
    def __init__(self, path: str):
        self.path = path
        self.update()

    def update(self, path: str = ""):
        if path:
            self.path = path 
        # get filetype        
        t = self.path.split('.')[-1]  
        f = open(self.path, mode='r', encoding='utf-8')
        # parse
        j = "" 
        if t == "json":
            j = json.loads(str(f.read()))
        elif t == "xml":
            return # TODO
        else:
            print("Unsupported Config Encoding: ", t) # ERROR
            return
        # update self 
        self.id = j["c"]["id"]
        self.secret = j["c"]["secret"]

import hashlib, requests, random, base64, string

class Spotify:
    def __init__(self, config: Config, token: str = ""):
        self.token = token
        self.authed = False 
        self.c = config

        if not token:
            # returns state bool
            self.authed = self.auth()

    def safehash(self, c: str):
        h = hashlib.sha256()
        h.update(bytes(c, 'ascii'))
        psuedosafe = base64.urlsafe_b64encode(h.digest()).decode('ascii')
        safe = psuedosafe.replace('=', '')
        return safe
   
    def auth(self):
        if self.authed:
            return

        seed = str(random.random())
        self.cookie = self.safehash(seed)
        
        self.verifier = (''.join(random.choice(string.ascii_letters) for x in range(43))) 
        getA = {
            "client_id": self.c.id,
            "response_type": "code",
            "redirect_uri": "http://localhost:1337/redirect",
            "state": self.cookie, # not nessecarily required, given that pyspot is 1:1
            "scope": "user-read-currently-playing",
            "code_challenge_method": "S256",
            "code_challenge": self.safehash(self.verifier) 
        }
        getR = requests.get(
                "https://accounts.spotify.com/authorize",
                params = getA
        ) 
        if getR.status_code != 200:
            print("err | auth() response code: ", str(getR.status_code)) # ERROR
            return False

        doAuthFlow(1337, getR.url)
        
        code = ""
        with open("/tmp/pyspot/code.txt", 'r') as f:
            code = f.read()
        
        m = f"{self.c.id}:{self.c.secret}".encode('ascii')
        b64m = base64.b64encode(m).decode('ascii')

        postHdrs = {
                "Authorization": "Basic "+b64m,
                "Content-Type": "application/x-www-form-urlencoded"
        } 
        postParams = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "http://localhost:1337/redirect",
                "client_id": self.c.id,
                "code_verifier": self.verifier
        }
        postR = requests.post(
                "https://accounts.spotify.com/api/token",
                params = postParams,
                headers = postHdrs
        )

        if postR.status_code != 200:
            print("err | auth() response code: ", str(postR.status_code), postR.text) # ERROR
            return False
        
        pj = json.loads(postR.text)
        self.token = pj["access_token"]
        self.rtoken = pj["refresh_token"]
        self.expire = pj["expires_in"]
        return True

    def pull_track(self):
        if not authed:
            self.auth()


        return

def main():
    c = Config("./test.cfg.json")
    s = Spotify(c)
 
if __name__ == '__main__':
    main()
