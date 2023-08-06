# coding=utf-8
# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2020
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import requests
from .client_errors import AuthorizationError

class EntitlementClient:

    def __init__(self, url, bearer_token, instance_id):
        self.bearer_token = bearer_token
        self.instance_id = instance_id
        self.entitlement_url = url + '/v1/entitlements'
        
    def is_entitled(self):
        response = self.get_entitlements()
        plan_name = None
        msg = "You are not authorized to access AI OpenScale instance {}".format(self.instance_id)
        try:
            entitlements = response['entitlements']
            if 'ai_openscale' not in entitlements:
                raise AuthorizationError(msg)

            instances = entitlements['ai_openscale']
            if len(instances) <= 0:
                raise AuthorizationError(msg)

            current_instance = None
            for instance in instances:
                if self.instance_id == instance['id']:
                    current_instance = instance
                    break

            if not current_instance:
                raise AuthorizationError(msg)

            instance_id = current_instance['id']
            if 'plan_name' in current_instance:
                plan_name = current_instance['plan_name']
            if len(instance_id) <= 0:
                raise AuthorizationError(msg)   
        except KeyError:
            raise AuthorizationError("Failed to authenticate")
        
        return plan_name

    def get_entitlements(self):
        
        response = requests.get(self.entitlement_url, headers=self.get_headers())
        if not response.ok:
            raise AuthorizationError("Failed to authenticate")

        return response.json()

    def get_headers(self):
        headers = {}
        headers["Authorization"] = "Bearer " + self.bearer_token
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        return headers
