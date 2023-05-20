from yaml import safe_load
from typing import Dict
import requests
import base64

class SpotifyOAuth:
    def __init__(self, CONFIG):
        self.CONFIG:Dict[str, Dict] = CONFIG
        self.CONSTANTS = self.CONFIG['constants']
        self.ENDPOINTS = self.CONFIG['endpoints']
        self._get_creds()


    def _get_creds(self):
        with open(self.CONFIG['creds']['path'], 'r') as f:
            self.API_CREDS:Dict[str,str] = safe_load(f)
    

    def _build_oauth_headers(self):
        client_key = self.API_CREDS['client_id'] + ':' + self.API_CREDS['client_secret']
        client_key = str(base64.b64encode(client_key.encode('utf-8')), 'utf-8')
        self.HEADERS = {
            'Authorization': f'Basic {client_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }


    def request_access_token(self):
        self._build_oauth_headers()
        data = {
            'grant_type': 'client_credentials'
        }
        self.oauth_response = requests.post(
            url=self.ENDPOINTS['oauth'],
            headers=self.HEADERS,
            data=data
        )
        self.oauth_response.raise_for_status()
        self.access_token = self.oauth_response.json()['access_token']


    def build_token_headers(self):
        """Headers for GET with access token from OAuth"""
        self.token_headers = {
            'Authorization': f'Bearer {self.access_token}'
        }