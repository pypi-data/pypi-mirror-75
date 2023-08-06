import json
import requests


def get_fifa_token(client_id, client_secret, fifa_token_endpoint="https://fifa.media-saturn.com/login/oauth/token"):
    """
    :param client_id: str
    :param client_secret: str
    :param fifa_token_endpoint: str
    :return: tuple (error, bearer_token). If no error: (None, "Bearer 12334...."). If error: ("Error message", None)
    """
    try:
        data = {'grant_type': 'client_credentials'}
        try:
            access_token_response = requests.post(fifa_token_endpoint, data=data, auth=(client_id, client_secret))
        except Exception as ex:
            return 'Get new FIFA bearer token failed: {}'.format(ex), None

        status_code = access_token_response.status_code

        # Check response code
        if status_code != 200:
            return 'FIFA API call not successful: code {}, response {}'.format(status_code, access_token_response.text), None

        result_body = json.loads(access_token_response.content)
        bearer_token = "Bearer {}".format(result_body["access_token"])
        return None, bearer_token

    except Exception as exc:
        return "Unexpected error: {}".format(exc), None

