import ConfigParser
import os.path
from fedora.client import AccountSystem, AuthError

class UserParser:

    def __init__(self):
        self.username = None
        self.password = None
        self.config = ConfigParser.RawConfigParser()
        try:
            self.config.read('fas_credentials.cfg')
            self.username = self.config.get('fas', 'username').strip('\'')
            self.password = self.config.get('fas', 'password').strip('\'')
            self.check_config()
        except:
            print("[*] Invalid / Missing Configuration file.")
    def check_config(self):
            if self.username.strip('\'') == 'FAS_USERNAME_HERE':
                print("[*] Please enter FAS credentials in fas_credentials.cfg")
                return False
            else:
                return True

    def user_active(self, name):
        user_json = dict()
        account = AccountSystem(username=self.username,
                            password=self.password)
        try:
            user_json = account.person_by_username(name)
        except AuthError:
            print("[*] Invalid Username / Password")
            return 1
        try:
            if user_json['status'] == 'active':
                return True
            else:
                return False
        except KeyError:
            return False
