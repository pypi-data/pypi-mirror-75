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
import warnings

from ibm_cloud_sdk_core import BaseService

from ibm_watson_openscale.base_classes.tables import Table
from .utils import *
from ibm_watson_openscale.base_classes.watson_open_scale_v2 import BusinessApplications as BaseBusinessApplications

if TYPE_CHECKING:
    from .client import WatsonOpenScaleV2Adapter
    from ibm_watson_openscale.base_classes.watson_open_scale_v2 import DetailedResponse, BusinessMetric, PayloadField

_DEFAULT_LIST_LENGTH = 50
warnings.filterwarnings("always", category=UserWarning)


class BusinessApplications(BaseBusinessApplications):
    """
    Manages Business Applications.
    """

    def __init__(self, ai_client: 'WatsonOpenScaleV2Adapter') -> None:
        validate_type(ai_client, 'ai_client', BaseService, True)
        self._ai_client = ai_client
        super().__init__(watson_open_scale=self._ai_client)

    def show(self, limit: int = 10) -> None:
        """
        Show monitor definitions. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>>  client.business_applications.show()
        >>>  client.business_applications.show(limit=20)
        >>>  client.business_applications.show(limit=None)
        """
        validate_type(limit, u'limit', int, False)

        response = self.list()

        records = [[business_app.metadata.id,
                    business_app.metadata.created_at,
                    business_app.entity.name,
                    [metric.name for metric in business_app.entity.business_metrics],
                    business_app.entity.business_metrics_monitor_definition_id,
                    business_app.entity.business_metrics_monitor_instance_id,
                    business_app.entity.business_payload_data_set_id,
                    business_app.entity.correlation_monitor_instance_id,
                    business_app.entity.description,
                    [field.name for field in business_app.entity.payload_fields],
                    business_app.entity.status.state,
                    business_app.entity.subscription_ids,
                    business_app.entity.transaction_batches_data_set_id,
                    ]
                   for business_app in response.result.business_applications]
        columns = ['id', 'created_at', 'name', 'business_metrics', 'business_metrics_monitor_definition_id',
                   'business_metrics_monitor_instance_id', 'business_payload_data_set_id',
                   'correlation_monitor_instance_id', 'description', 'payload_fields', 'status',
                   'subscription_ids', 'transaction_batches_data_set_id']

        Table(columns, records).list(
            limit=limit,
            default_limit=_DEFAULT_LIST_LENGTH,
            title="Business applications"
        )

    def add(self,
            name: str,
            description: str,
            payload_fields: List['PayloadField'],
            business_metrics: List['BusinessMetric'],
            subscription_ids: List[str] = None,
            business_metrics_monitor_definition_id: str = None,
            business_metrics_monitor_instance_id: str = None,
            correlation_monitor_instance_id: str = None,
            business_payload_data_set_id: str = None,
            transaction_batches_data_set_id: str = None,
            background_mode: bool = True) -> Union['DetailedResponse', Optional[dict]]:
        """
        Add business application.

        :param str name: name fo the business application.
        :param str description: description fo the business application.
        :param List[PayloadField] payload_fields:
        :param List[BusinessMetric] business_metrics:
        :param List[str] subscription_ids: (optional)
        :param str business_metrics_monitor_definition_id: (optional)
        :param str business_metrics_monitor_instance_id: (optional)
        :param str correlation_monitor_instance_id: (optional)
        :param str business_payload_data_set_id: (optional) Unique identifier of
               the data set (like scoring, feedback or business payload).
        :param str transaction_batches_data_set_id: (optional) Unique identifier of
               the data set (like scoring, feedback or business payload).
        :param background_mode: if set to True, run will be in asynchronous mode, if set to False
                it will wait for result (optional)
        :type background_mode: bool
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse with `BusinessApplicationResponse` result

        A way you might use me is:

        >>> payload = {
                 "name": "Credit Risk Application",
                 "description": "Test Business Application",
                 "payload_fields": [
                     {
                         "name": "LoanDuration",
                         "type": "number",
                         "description": "Duration of the loan"
                     }...
                 ],
                 "business_metrics": [
                     {
                         "name": "Accepted Credits",
                         "description": "Accepted Credits Daily",
                         "expected_direction": "increasing",
                         "thresholds": [
                             {
                                 "type": "lower_limit",
                                 "default": 55,
                                 "default_recommendation": "string"
                             }
                         ],
                         "required": False,
                         "calculation_metadata": {
                             "field_name": "Accepted",
                             "aggregation": "sum",
                             "time_frame": {
                                 "count": 1,
                                 "unit": "day"
                             }
                         }
                     }...
                 ],
                 "subscription_ids": [
                     '997b1474-00d2-4g05-ac02-287ebfc603b5'
                 ]
              }
        >>>  business_application_details = client.business_applications.add(background_mode=False, **payload)
        """
        # note: check if transaction_id_field is set in subscription, it is needed to run business application correctly
        for subscription_id in subscription_ids:
            subscription_info = self._ai_client.subscriptions.get(subscription_id=subscription_id)
            try:
                subscription_info.result.entity.asset_properties.transaction_id_field
            except AttributeError:
                warnings.warn(
                    message="Subscription: {} does not have transaction_id_column set. "
                            "To be able to correctly run a business application, please set "
                            "a \"transaction_id_column\" during subscription creation.".format(
                        subscription_info.result.metadata.id))

        response = super().add(name=name, description=description, payload_fields=payload_fields,
                               business_metrics=business_metrics, subscription_ids=subscription_ids,
                               business_metrics_monitor_definition_id=business_metrics_monitor_definition_id,
                               business_metrics_monitor_instance_id=business_metrics_monitor_instance_id,
                               correlation_monitor_instance_id=correlation_monitor_instance_id,
                               business_payload_data_set_id=business_payload_data_set_id,
                               transaction_batches_data_set_id=transaction_batches_data_set_id)

        business_application_id = response.result.metadata.id

        if background_mode:
            return response
        else:
            def check_state() -> dict:
                details = self.get(business_application_id=business_application_id)
                return details.result.entity.status.state

            def get_result() -> Union[Tuple[str, Union[None, str], 'DetailedResponse']]:
                details = self.get(business_application_id=business_application_id)
                state = details.result.entity.status.state

                if state in [StatusStateType.ACTIVE]:
                    return "Successfully finished adding business application", None, details
                else:
                    return "Add business application failed with status: {}".format(state), \
                           'Reason: {}'.format(["code: {}, message: {}".format(error.code, error.message) for error in
                                                details.result.entity.status.failure.errors]), details

            return print_synchronous_run(
                'Waiting for end of adding business application {}'.format(business_application_id),
                check_state,
                get_result=get_result,
                success_states=[StatusStateType.ACTIVE]
            )

    def delete(self,
               business_application_id: str,
               background_mode: bool = True) -> Union['DetailedResponse', Optional[dict]]:
        """
        Delete business application.

        :param str business_application_id: ID of the business application.
        :param background_mode: if set to True, run will be in asynchronous mode, if set to False
                it will wait for result (optional)
        :type background_mode: bool
        :return: A `DetailedResponse` containing the result, headers and HTTP status code.
        :rtype: DetailedResponse

        A way you may use me:

        >>>  quality_monitor_details = client.business_applications.delete(
                 business_application_id='997b1474-00d2-4g05-ac02-287ebfc603b5'
              )
        """
        response = super().delete(business_application_id=business_application_id)

        if background_mode:
            return response
        else:
            def check_state() -> dict:
                details = self.list()
                if business_application_id not in str(details.result):
                    return StatusStateType.FINISHED
                else:
                    return StatusStateType.ACTIVE

            def get_result() -> Union[Tuple[str, Union[None, str], 'DetailedResponse']]:
                details = self.list()
                if business_application_id not in str(details.result):
                    state = StatusStateType.FINISHED
                else:
                    state = StatusStateType.ACTIVE

                if state in [StatusStateType.FINISHED]:
                    return "Successfully finished deleting business application", None, response
                else:
                    return "Delete business application failed", 'Reason: None', response  # TODO: Need to show the reason.

            return print_synchronous_run(
                'Waiting for end of deleting business application {}'.format(business_application_id),
                check_state,
                get_result=get_result,
                success_states=[StatusStateType.FINISHED]
            )
