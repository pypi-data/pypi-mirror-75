"""
NeurodataLab LLC 02.11.2019
Created by Andrey Belyaev
"""
import json
import os
import os.path as osp

from ndlapi.api._auth.AuthCredentials import AuthCredential
from ndlapi.api._utils import read_binary
from ndlapi.api._utils.error_utils import check_connection


class SslCredential:
    def __init__(self, user_key, chain, root_ca):
        self.user_key = read_binary(user_key)
        self.user_cert = read_binary(chain)
        self.server_ca = read_binary(root_ca)

    def key(self):
        return self.user_key

    def cert(self):
        return self.user_cert

    def ca(self):
        return self.server_ca


def create_credentials(api_keys_folder, api_url='ru1.recognition.api.neurodatalab.dev', api_port='30051'):
    # Initialize paths
    cert_home = api_keys_folder

    # Find certificate files
    cert_files = os.listdir(cert_home)
    client_crt_file, client_key_file, ca_crt_file, root_json_filepath = [''] * 4
    try:
        client_key_file = list(filter(lambda p: p.startswith('client') and p.endswith('.key'), cert_files))[0]
        client_crt_file = list(filter(lambda p: p.startswith('client') and p.endswith('.crt'), cert_files))[0]
        ca_crt_file = list(filter(lambda p: p.startswith('ca') and p.endswith('.crt'), cert_files))[0]
        root_json_filepath = list(filter(lambda p: p.startswith('root') and p.endswith('json'), cert_files))[0]
    except:
        print("You don't have all certificate's files. "
              "Please check for client_*.key, client_*.crt, ca_*.crt, root_*.json")
        exit(0)

    with open(osp.join(cert_home, root_json_filepath), 'r') as f:
        d = json.load(f)
        if 'apiUrl' in d and d['apiUrl'] != 'recognition.api.neurodatalab.dev':
            api_url = d['apiUrl']

    check_connection(api_url, api_port)

    # Create common auth credentials
    ssl_auth_info = SslCredential(osp.join(cert_home, client_key_file),
                                  osp.join(cert_home, client_crt_file),
                                  osp.join(cert_home, ca_crt_file))
    auth = AuthCredential('%s:%s' % (api_url, api_port), osp.join(cert_home, root_json_filepath), ssl_auth_info)

    return auth
