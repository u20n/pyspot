import typing
import io
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
class AuthServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path).query
        pairs = parsed.split('&')
        final = {}
        for i in pairs:
            x = i.split('=')
            final[x[0]] = x[1]
        # code is here, if you want it (for confirm page)
        with open("/tmp/pyspot/code.txt", 'w') as f:
            f.write(final["code"])

        self.send_response(200)
        self.send_header("Content-Type", "text/html");
        self.end_headers() 
  
def doAuthFlow(port: int, url: str):
    ws = HTTPServer(("localhost", port), AuthServer)
    ws.socket.settimeout(15)
    webbrowser.open_new_tab(url)
    ws.handle_request()
    
import socket
import json
#import xml TODO
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

import hashlib
import requests
import random
import base64
import string

class Spotify:
    def __init__(self, config: Config, token: str = ""):
        self.token = token
        self.authed = False 
        self.c = config

        if not token:
            # returns state bool
            self.authed = self.auth()
    
    def gencookie(self, c: str):
        h = hashlib.sha256()
        h.update(bytes(c, 'ascii'))
        return base64.urlsafe_b64encode(h.digest()).decode('ascii')
    
    def genverifier(self, c: str):
        h = hashlib.sha256()
        h.update(bytes(c, 'ascii'))
        psuedosafe = base64.urlsafe_b64encode(h.digest()).decode('ascii')
        safe = psuedosafe.replace('=', '')
        return safe
   
    def auth(self):
        if self.authed:
            return

        seed = str(random.random())
        cookie = self.gencookie(seed)
        self.cookie = cookie

        l = string.ascii_letters
        self.verifier = (''.join(random.choice(l) for x in range(43))) 
        a = {
            "client_id": self.c.id,
            "response_type": "code",
            "redirect_uri": "http://localhost:1337/redirect",
            "state": cookie,
            "scope": "user-read-currently-playing",
            "code_challenge_method": "S256",
            "code_challenge": self.genverifier(self.verifier) 
        }
        r = requests.get(
                "https://accounts.spotify.com/authorize",
                params = a
        ) 
        if r.status_code != 200:
            print("err | auth() response code: ", str(r.status_code)) # ERROR
            return False

        doAuthFlow(1337, r.url)
        
        code = ""
        with open("/tmp/pyspot/code.txt", 'r') as f:
            code = f.read()
        
        m = f"{self.c.id}:{self.c.secret}"
        b = m.encode('ascii')
        b64b = base64.b64encode(b)
        b64m = b64b.decode('ascii')

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
        p = requests.post(
                "https://accounts.spotify.com/api/token",
                params = postParams,
                headers = postHdrs
        )

        if p.status_code != 200:
            print("err | auth() response code: ", str(p.status_code), p.text) # ERROR
            return False
        print(p.text)
    def pull_track(self):
        if not authed:
            self.auth() 
        return

def main():
    c = Config("./test.cfg.json")
    s = Spotify(c)
 
if __name__ == '__main__':
    main()
