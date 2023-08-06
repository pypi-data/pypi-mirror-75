"""
Wisdom is the user interaction with Whatify wisdom, it contains

"""
# Prediction is the way to productize the Ensemble created in the previous steps. Once an Ensemble is created,
# users can upload additional Datasources that may be used for predictions.
#
# ‘Prediction’ API includes querying of predictions (Get, List and Delete) and creating a Prediction to get predictions
# on existing Ensembles and uploaded Datasources.
import os
from typing import Dict, List

from toolkit_w.internal import utils
from toolkit_w.internal.api_requestor import APIRequestor
from toolkit_w.internal.whatify_response import WhatifyResponse
from toolkit_w.resources.api_resource import APIResource


class Wisdom(APIResource):
    _CLASS_PREFIX = 'foresights'

    @classmethod
    def get_wisdom_list_with_demo(cls, api_key: str = None) -> WhatifyResponse:
        """
        Gets the wisdoms list for the user with the demo wisdoms.

        Args:
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains mapping of wisdoms for the user.
        """
        requestor = APIRequestor()
        url = '{prefix}/with_demo'.format(prefix=cls._CLASS_PREFIX)
        response = requestor.get(url, api_key=api_key)['hits']
        return response

    @classmethod
    def get_wisdom(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Gets the wisdom data for the user by its ID

        Args:
            id (int): wisdom (foresight) ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: Contains wisdom data by ID for the user.
        """
        requestor = APIRequestor()
        url = '{prefix}/{id}'.format(prefix=cls._CLASS_PREFIX, id=id)
        response = requestor.get(url, api_key=api_key)
        return response

    @classmethod
    def delete(cls, id: int, api_key: str = None) -> WhatifyResponse:
        """
        Deletes a specific Wisdom.

        Args:
            id (int): Wisdom ID.
            api_key (Optional[str]): Explicit `api_key`, not required, if `Whatify.login()` was run prior.

        Returns:
            WhatifyResponse: "true" if deleted successfuly, raises WhtifyClientError otherwise.
        """
        return cls._delete(id, api_key)


