"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
from ndlapi.api._utils import read_binary


class AuthCredential:
    def __init__(self, target_host, token, ssl_credentials):
        self.server_host = target_host
        self.user_token = read_binary(token)
        self.ssl = ssl_credentials

    def token(self):
        return self.user_token.decode()

    def ssl_credentials(self):
        return self.ssl

    def host(self):
        return self.server_host
