# coding: utf-8

# Copyright 2020 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Tuple

from ibm_cloud_sdk_core import BaseService

from ibm_watson_openscale.base_classes.tables import Table
from .utils import *
from ibm_watson_openscale.base_classes.watson_open_scale_v2 import Subscriptions as BaseSubscriptions
from ibm_watson_openscale.base_classes.watson_open_scale_v2 import Asset, AssetPropertiesRequest, \
    AssetDeploymentRequest, RiskEvaluationStatus

if TYPE_CHECKING:
    from .client import WatsonOpenScaleV2Adapter
    from ibm_watson_openscale.base_classes.watson_open_scale_v2 import DetailedResponse

_DEFAULT_LIST_LENGTH = 50


# TODO: Add parameters validation in every method
class Subscriptions(BaseSubscriptions):
    """
    Manages Subscription instance.
    """

    def __init__(self, ai_client: 'WatsonOpenScaleV2Adapter') -> None:
        validate_type(ai_client, 'ai_client', BaseService, True)
        self._ai_client = ai_client
        super().__init__(watson_open_scale=self._ai_client)

    def show(self, limit: Optional[int] = 10) -> None:
        """
        Show service providers. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> client.subscriptions.show()
        >>> client.subscriptions.show(limit=20)
        >>> client.subscriptions.show(limit=None)
        """
        validate_type(limit, u'limit', int, False)

        response = self.list()

        records = [[subscription.entity.asset.asset_id,
                    subscription.entity.asset.name,
                    subscription.entity.data_mart_id,
                    subscription.entity.deployment.deployment_id,
                    subscription.entity.deployment.name,
                    subscription.entity.service_provider_id,
                    subscription.entity.status.state,
                    subscription.metadata.created_at,
                    subscription.metadata.id
                    ] for subscription in response.result.subscriptions]
        columns = ['asset_id', 'asset_name', 'data_mart_id', 'deployment_id', 'deployment_name',
                   'service_provider_id', 'status', 'created_at', 'id']

        Table(columns, records).list(
            limit=limit,
            default_limit=_DEFAULT_LIST_LENGTH,
            title="Subscriptions"
        )

    def add(self,
            data_mart_id: str,
            service_provider_id: str,
            asset: 'Asset',
            deployment: 'AssetDeploymentRequest',
            asset_properties: 'AssetPropertiesRequest' = None,
            risk_evaluation_status: 'RiskEvaluationStatus' = None,
            background_mode: bool = True) -> Union['DetailedResponse', Optional[dict]]:
        """
        Add a subscription to the model deployment.

        :param str data_mart_id: ID of the data_mart (required)
        :param str service_provider_id: ID of the service_provider (required)
        :param Asset asset: an Asset object with asset's information (required)
        :param AssetDeploymentRequest deployment: an AssetDeploymentRequest object with deployment's information (required)
        :param AssetPropertiesRequest asset_properties: (optional) Additional asset
               properties (subject of discovery if not provided when creating the
               subscription).
        :param RiskEvaluationStatus risk_evaluation_status: (optional)
        :param background_mode: if set to True, run will be in asynchronous mode, if set to False
                it will wait for result (optional)
        :type background_mode: bool
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `SubscriptionResponse` result

        A way you may use me:

        >>> from ibm_watson_openscale import *
        >>> added_subscription_info = cleint.subscriptions.add(
                data_mart_id='997b1474-00d2-4g05-ac02-287ebfc603b5',
                service_provider_id='997b1474-00d2-4g05-ac02-287ebfc603b5',
                asset=Asset(...),
                deployment=AssetDeploymentRequest(...),
                asset_properties=AssetPropertiesRequest(...),
             )
        """
        validate_type(data_mart_id, 'data_mart_id', str, True)
        validate_type(service_provider_id, 'service_provider_id', str, True)
        
        if self._ai_client.check_entitlements is True and self._ai_client.plan_name == self._ai_client.LITE_PLAN:
            total_subscriptions = self.list().result.subscriptions
            if len(total_subscriptions) >=5:
                raise Exception("You are not allowed to create more than 5 subscriptions for lite plan.")
        
        response = super().add(data_mart_id=data_mart_id, service_provider_id=service_provider_id, asset=asset,
                               deployment=deployment, asset_properties=asset_properties,
                               risk_evaluation_status=risk_evaluation_status)

        subscription_id = response.result.metadata.id

        if background_mode:
            return response
        else:
            def check_state() -> dict:
                details = self.get(subscription_id=subscription_id)
                return details.result.entity.status.state

            def get_result() -> Union[Tuple[str, Union[None, str], 'DetailedResponse']]:
                details = self.get(subscription_id=subscription_id)
                state = details.result.entity.status.state

                if state in [StatusStateType.ACTIVE]:
                    return "Successfully finished adding subscription", None, details
                else:
                    return "Add subscription failed with status: {}".format(state), \
                           'Reason: {}'.format(["code: {}, message: {}".format(error.code, error.message) for error in
                                                details.result.entity.status.failure.errors]), details

            return print_synchronous_run(
                'Waiting for end of adding subscription {}'.format(subscription_id),
                check_state,
                get_result=get_result,
                success_states=[StatusStateType.ACTIVE]
            )

    def delete(self,
               subscription_id: str,
               force: bool = None,
               background_mode: bool = True) -> Union['DetailedResponse', Optional[dict]]:
        """
        Delete subscription.

        :param str subscription_id: Unique subscription ID.
        :param bool force: (optional) force hard delete.
        :param background_mode: if set to True, run will be in asynchronous mode, if set to False
                it will wait for result (optional)
        :type background_mode: bool
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse

        A way you may use me:

        >>> client.subscriptions.delete(
                background_mode=False,
                subscription_id='997b1474-00d2-4g05-ac02-287ebfc603b5',
                force=True
             )
        """
        response = super().delete(subscription_id=subscription_id, force=force)

        if background_mode:
            return response
        else:
            def check_state() -> dict:
                details = self.list()
                if subscription_id not in str(details.result):
                    return StatusStateType.FINISHED
                else:
                    return StatusStateType.ACTIVE

            def get_result() -> Union[Tuple[str, Union[None, str], 'DetailedResponse']]:
                details = self.list()
                if subscription_id not in str(details.result):
                    state = StatusStateType.FINISHED
                else:
                    state = StatusStateType.ACTIVE

                if state in [StatusStateType.FINISHED]:
                    return "Successfully finished deleting subscription", None, response
                else:
                    return "Delete subscription failed", 'Reason: None', response  # TODO: Need to show the reason.

            return print_synchronous_run(
                'Waiting for end of deleting subscription {}'.format(subscription_id),
                check_state,
                get_result=get_result,
                success_states=[StatusStateType.FINISHED]
            )
