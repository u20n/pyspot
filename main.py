import json
import typing
import hashlib
import requests
import random

class Config:
    def __init__(self, path: str):
        self.path = path
        self.update()

    def update(self, path: str = ""):
        if path:
            self.path = path 
        # get filetype        
        t = self.path.split('.')[-1] 
        # read
        f = open(self.path, mode='r', encoding='utf-8')
        # parse
        j = "" 
        if t == "json":
            j = json.loads(str(f.read()))
        elif t == "xml":
            return # TODO
        else:
            print("Unsupported Config Encoding: ", t)
            return
        # update self 
        self.id = j["c"]["id"]
        self.secret = j["c"]["secret"]

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
        h.update(bytes(c, 'utf-8'))
        return h.hexdigest()

    def auth(self):
        if self.authed:
            return

        seed = str(random.random())
        print("seed: ", seed) # DEBUG
        
        cookie = self.gencookie(str(random.random()))
        print("cookie: ", cookie) # DEBUG
        self.cookie = cookie

        a = json.dumps({
            "client_id": self.c.id,
            "response_type": "token",
            "redirect_uri": "...",
            "state": cookie,
            "scope": "user-read-currently-playing"
        })
        #r = requests.get("https://api.spotify.com/v1/me/player", 
        #if r.status_code != 200:
        #    print("err | auth() response code: ", str(r.status_code))
        #     return False

    def pull_track(self):
        if not authed:
            self.auth() 
        return

def main():
    c = Config("./test.cfg.json")
    s = Spotify(c)
 
if __name__ == '__main__':
    main()

