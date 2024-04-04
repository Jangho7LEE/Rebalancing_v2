import json
from json import JSONDecodeError
import requests
import logging
import time
from MyDart.lib.utils import cleanNoneValue
from MyDart.lib.utils import check_required_parameter
from MyDart.lib.utils import encoded_string
from MyDart.lib.errors import ClientError, ServerError


class API(object):
    def __init__(self,
                 key: str,
                 base_url = None
                 ) -> None:
        if not key:
            raise ValueError("Must input your key!!!")
        self.key = key
        self.session = requests.Session()
        if base_url:
            self.base_url = base_url

    def query(self, url_path, payload=None):
        return self.send_request("GET", url_path, payload=payload)
         
    def limit_request(self, http_method, url_path, payload=None):
        """limit request is for those endpoints require API key in the header"""
        check_required_parameter(self.key, "apiKey")
        return self.send_request(http_method, url_path, payload=payload)
    
    def content_request(self, http_method, url_path, payload=None):
        """content_request is for download zip files in the endpoints require API key in the header"""
        return self.send_request(http_method, url_path, payload=payload, download=True)
    
    def send_request(self, http_method, url_path, payload=None, special =False, download=False):
        time.sleep(0.7)
        if payload is None:
            payload = {'crtfc_key' : self.key}
        else:
            payload['crtfc_key'] = self.key
            
        url = self.base_url + url_path
        logging.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload, special),
            }
        )
        try:
            response = self._dispatch_request(http_method)(**params)
        except:
            data ={'status': '-1'}
            return data
        logging.debug("raw response from server:" + response.text)
        self._handle_exception(response)
        if download:
            try:
                data = response.content
            except ValueError:
                data = response.text
        else:
            try:
                data = response.json()
            except ValueError:
                data = response.text
        
        return data
    
    def _dispatch_request(self, http_method):
        return {
            "GET": self.session.get,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "POST": self.session.post,
        }.get(http_method, self.session.get)
    

    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, response.headers)
            raise ClientError(status_code, err["code"], err["msg"], response.headers)
        raise ServerError(status_code, response.text)
    
    def _prepare_params(self, params, special=False):
        return encoded_string(cleanNoneValue(params), special)