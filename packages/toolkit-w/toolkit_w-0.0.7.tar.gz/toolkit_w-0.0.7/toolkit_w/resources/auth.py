import toolkit_w
from toolkit_w.internal import UserToken
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.whatify_response import WhatifyResponse


def authenticate(username: str, password: str) -> WhatifyResponse:
    """
    Authenticates user and stores temporary token in `fireflyai.token`.

    Other modules automatically detect if a token exists and use it, unless a user specifically provides a token
    for a specific request.
    The token is valid for a 24-hour period, after which this method needs to be called again in order to generate
    a new token.

    Args:
        username (str): Username.
        password (str): Password.

    Returns:
        WhatifyResponse: Empty WhatifyResponse if successful, raises FireflyError otherwise.
    """
    url = 'login'

    requestor = APIRequestor()
    response = requestor.post(url, body={'username': username, 'password': password, 'tnc': None}, api_key="")
    toolkit_w.token = response['token']
    return WhatifyResponse(status_code=response.status_code, headers=response.headers)
