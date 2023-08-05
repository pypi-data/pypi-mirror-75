from typing import Union


class OrkgResponse(object):

    @property
    def succeeded(self) -> bool:
        return str(self.status_code)[0] == '2'

    def __init__(self, response=None, status_code: str = None, content: Union[list, dict] = None, url: str = None):
        if response is None and status_code is None and content is None and url is None:
            raise ValueError("either response should be provided or content with status code")
        if response is not None:
            self.status_code = response.status_code
            self.content = response.json() if len(response.content) > 0 else response.content
            self.url = response.url
        if status_code is not None and content is not None:
            self.status_code = status_code
            self.content = content
            self.url = url

    def __repr__(self):
        return "%s %s" % ("(Success)" if self.succeeded else "(Fail)", self.content)

    def __str__(self):
        return self.content
