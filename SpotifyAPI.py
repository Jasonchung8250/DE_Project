import requests
import pandas
import base64
from datetime import datetime,timedelta
import json


class SpotifyAPI(object):
    access_token = ''
    access_token_expires = ''
    client_id = ''
    client_secret = ''
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_token_header(self):
        #returns a base64 string (not bytes)
        if self.client_id == '' or self.client_secret == '':
            raise Exception("client_id or client_secret has not been updated")
        client_creds = "%s:%s" % (self.client_id, self.client_secret)
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return {
        "Authorization" : f"Basic {client_creds_b64.decode()}"
}
    
    
    def get_token_data(self):
        return {
        "grant_type" : "client_credentials"
        }
    
    def perform_auth(self):
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        token_url = self.token_url
        
        r = requests.post(token_url, data = token_data, headers = token_header)
        valid_request = r.status_code in range(200,299) #This is to check if status_code is valid
        if valid_request:
            token_response_data = r.json() #r.json() returns a dictionary
            now = datetime.now()
            access_token = token_response_data['access_token']
            expires_in = token_response_data['expires_in']
            expires = now + timedelta(seconds=expires_in)
            self.access_token_expires = expires
            self.access_token = access_token
            return "Success"
        return "Failed"