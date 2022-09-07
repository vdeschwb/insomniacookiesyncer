import os
import json
from datetime import datetime

class InsomniaCookieInjector:
    __cookies_filepath = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Insomnia\insomnia.CookieJar.db')

    def __init__(self):
        pass

    def get_cookies(self):
        cookies = []
        with open(self.__cookies_filepath, "r") as f:
            for l in f.readlines():
                jar = json.loads(l)
                cookies += jar['cookies']
        return cookies

    def load(self, cookies):
        # Load jars
        jars = []
        with open(self.__cookies_filepath, "r") as f:
            for l in f.readlines():
                jars.append(json.loads(l))

        synced = []

        # Inject new values into jars
        for (domain, key, value) in cookies:
            for jar_index in range(len(jars)):
                cookies = jars[jar_index]['cookies']
                existing = next(iter([c for c in cookies if c["key"] == key and c["domain"] == domain]), None)
                if existing != None:
                    new = {"key": key, "value": value, "domain": domain, "creation": datetime.utcnow().isoformat()[:-3]+'Z', "id": existing["id"], "expires": None}
                    jars[jar_index]["cookies"] = [c for c in cookies if c["key"] != key or c["domain"] != domain] + [new]
                    synced.append(new)
                else:
                    pass
        
        # Write updated jars to disk
        with open(self.__cookies_filepath, "w") as f:
            f.writelines([json.dumps(jar) + '\n' for jar in jars])

        return synced
