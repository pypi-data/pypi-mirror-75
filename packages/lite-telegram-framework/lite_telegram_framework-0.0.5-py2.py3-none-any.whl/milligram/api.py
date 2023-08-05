import requests


class Telegram:
    url_template = 'https://api.telegram.org/bot{token}/{method_name}'

    def __init__(self, token):
        self.token = token

    def _post(self, method_name, data):
        resp = requests.post(
            self.url_template.format(token=self.token, method_name=method_name),
            json=data
        )
        return resp.json()

    def get_me(self):
        return self._post('getMe', {})
