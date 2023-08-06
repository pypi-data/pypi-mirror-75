import subprocess
import google.auth
import google.oauth2.credentials
import google.oauth2.id_token
import google.auth.transport.requests
import time
import jwt
import urllib
import requests
import json

'''
Links:
- https://cloud.google.com/run/docs/authenticating/service-to-service
- https://readthedocs.org/projects/google-auth/downloads/pdf/stable/
- https://medium.com/@stephen.darling/oauth2-authentication-with-google-cloud-run-700015a092c2
- https://medium.com/google-cloud/authenticating-using-google-openid-connect-tokens-e7675051213b
'''


class GCPBearerToken(object):
    def __init__(self, authentication_method, target_url=None, path_to_service_account_file=None, service_account_dictionary=None):
        # 1. "gcloud-sdk": from local machine via gcloud sdk
        # 2. "service-account-file": from a local service-account json file
        # 3. "service-account-dictionary": from a parsed service-account json file
        # 4. "cloudrun-to-cloudrun": https://cloud.google.com/run/docs/authenticating/service-to-service
        # 5. "compute-default":  App Engine, Cloud Run, ‘Compute Engine‘_, or has application default credentials set via GOOGLE_APPLICATION_CREDENTIALS environment variable

        self.__token = None
        self.__exp = None
        self.authentication_method = authentication_method
        self.target_url = target_url
        self.path_to_service_account_file = path_to_service_account_file
        self.service_account_dictionary = service_account_dictionary

        allowed_methods = ["gcloud-sdk", "service-account-file", "service-account-dictionary", "cloudrun-to-cloudrun", "compute-default"]

        # Validate authentication_method:
        if authentication_method not in allowed_methods:
            raise ValueError("authentication_method must be one of {}".format(allowed_methods))

        # Validate required fields:
        if authentication_method != "gcloud-sdk" and target_url is None:
            raise ValueError("Please specify 'target_url' for authentication_method={}".format(authentication_method))

        if authentication_method == "service-account-file" and path_to_service_account_file is None:
            raise ValueError("authentication_method='service-account-file' requires the field 'path_to_service_account_file'")

        if authentication_method == "service-account-dictionary" and service_account_dictionary is None:
            raise ValueError("authentication_method='service-account-dictionary' requires the field 'service_account_dictionary'")

    # ****** gloucd sdk ************************************************************************************************
    @staticmethod
    def __create_from_gcloud_sdk():
        bash_result = subprocess.run(['gcloud', 'auth', 'print-identity-token'], stdout=subprocess.PIPE)
        token = bash_result.stdout
        return token.decode("utf-8")
    # ******************************************************************************************************************

    # ****** service accounts ******************************************************************************************
    @staticmethod
    def __read_sa_file(sa_key_path):
        with open(sa_key_path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def __create_signed_jwt(credentials, service_url):
        iat = time.time()
        exp = iat + 3600
        payload = {
            'iss': credentials['client_email'],
            'sub': credentials['client_email'],
            'target_audience': service_url,
            'aud': 'https://www.googleapis.com/oauth2/v4/token',
            'iat': iat,
            'exp': exp
        }
        additional_headers = {'kid': credentials['private_key_id']}
        return jwt.encode(payload, credentials['private_key'], headers=additional_headers, algorithm='RS256')

    @staticmethod
    def __exchange_jwt_for_token(signed_jwt):
        body = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': signed_jwt
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_request = requests.post(
            url='https://www.googleapis.com/oauth2/v4/token',
            headers=headers,
            data=urllib.parse.urlencode(body)
        )
        result = token_request.json()
        return result['id_token']

    def __create_from_sa(self, credentials):
        # Create signed jwt:
        signed_jwt = self.__create_signed_jwt(credentials, self.target_url)
        # Get id token:
        return self.__exchange_jwt_for_token(signed_jwt)
    # ******************************************************************************************************************

    # ****** cloudrun to cloudrun **************************************************************************************
    def __create_from_cr_to_cr(self):
        # Set up metadata server request
        # See https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature
        metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='
        token_request_url = metadata_server_token_url + self.target_url
        token_request_headers = {'Metadata-Flavor': 'Google'}
        # Fetch the token
        token_response = requests.get(token_request_url, headers=token_request_headers)
        return token_response.content.decode("utf-8")
    # ******************************************************************************************************************

    # ****** cloudrun to cloudrun **************************************************************************************
    def __create_from_compute_default(self):
        request = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(request, self.target_url)
    # ******************************************************************************************************************

    @staticmethod
    def __get_token_exp(id_token):
        url = "https://oauth2.googleapis.com/tokeninfo?id_token={}".format(id_token)
        r = requests.get(url=url)
        token_info = json.loads(r.content.decode('utf-8'))
        return float(token_info.get("exp"))

    def get_token(self):
        time_now = time.time()
        # Check if token needs initial creation or an update:
        if (self.__token is None) or (self.__exp is None) or (time_now >= self.__exp):
            if self.authentication_method == "gcloud-sdk":
                self.__token = self.__create_from_gcloud_sdk()
            elif self.authentication_method == "service-account-file":
                credentials = self.__read_sa_file(self.path_to_service_account_file)
                self.__token = self.__create_from_sa(credentials)
            elif self.authentication_method == "service-account-dictionary":
                self.__token = self.__create_from_sa(self.service_account_dictionary)
            elif self.authentication_method == "cloudrun-to-cloudrun":
                self.__token = self.__create_from_cr_to_cr()
            elif self.authentication_method == "compute-default":
                self.__token = self.__create_from_compute_default()
            else:
                pass
            self.__exp = self.__get_token_exp(self.__token)
        return self.__token

