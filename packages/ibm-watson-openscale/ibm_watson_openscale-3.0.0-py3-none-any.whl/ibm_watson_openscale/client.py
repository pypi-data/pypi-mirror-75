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

from .business_applications import BusinessApplications
from .data_marts import DataMarts
from .data_sets import DataSets
from .monitor_definitions import MonitorDefinitions
from .monitor_instances import MonitorInstances
from .service_providers import ServiceProviders
from .subscriptions import Subscriptions
from .utils import *
from .utils.entitlement_client import EntitlementClient 
from ibm_watson_openscale.base_classes.watson_open_scale_v2 import WatsonOpenScaleV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, CloudPakForDataAuthenticator


##############################################################################
# Service
##############################################################################
class WatsonOpenScaleV2Adapter(WatsonOpenScaleV2):
    """
        Watson OpenScale client.

        :var version: Returns version of the python library.
        :vartype version: str

        :var authenticator: Returns passed authenticator.
        :vartype authenticator: IAMAuthenticator, CloudPakForDataAuthenticator

        :var data_marts: Manages data_marts module
        :vartype data_marts: ibm_watson_openscale.data_marts.DataMarts

        :var service_providers: Manages service_providers module
        :vartype service_providers: ibm_watson_openscale.service_providers.ServiceProviders

        :var subscriptions: Manages subscriptions module
        :vartype subscriptions: ibm_watson_openscale.subscriptions.Subscriptions

        :var data_sets: Manages data_sets module
        :vartype data_sets: ibm_watson_openscale.data_sets.DataSets

        :var monitor_definitions: Manages monitor_definitions module
        :vartype monitor_definitions: ibm_watson_openscale.monitor_definitions.MonitorDefinitions

        :var monitor_instances: Manages monitor_instances module
        :vartype monitor_instances: ibm_watson_openscale.monitor_instances.MonitorInstances

        :var business_applications: Manages business_applications module
        :vartype business_applications: ibm_watson_openscale.business_applications.BusinessApplications

        A way you might use me is:

        >>> from ibm_watson_openscale import APIClient
        >>> client = APIClient(authenticator=authenticator, service_url=service_url) # client will use default service_instance_id
        >>> client = APIClient(authenticator, service_url) # client will use default service_url and default service_instance_id
        >>> client = APIClient(authenticator=authenticator, service_url=service_url, service_instance_id=service_instance_id)
        >>> client = APIClient(authenticator, service_url, service_instance_id)
        """

    DEFAULT_SERVICE_URL = 'https://api.aiopenscale.cloud.ibm.com'
    LITE_PLAN = 'lite'

    @classmethod
    def new_instance(cls, service_name: str = None) -> 'WatsonOpenScaleV2Adapter':
        """
        This class method should be used only if you have stored your credentials
        in the separate file or in the ENV variable.

        :param service_name: Unique name of the service to configure.
        :paramtype service_name: str
        :return: ibm_watson_openscale.APIClient

        A way you might use me is:

        >>> from ibm_watson_openscale import APIClient
        >>> client = APIClient.new_instance(service_name='openscale-1')
        >>> client = APIClient.new_instance(service_name='openscale-2')
        >>> client = APIClient.new_instance('openscale')
        """
        validate_type(service_name, 'service_name', str, True)
        service = super().new_instance(service_name=service_name)
        return service

    def __init__(self,
                 authenticator: Optional[Union['IAMAuthenticator', 'CloudPakForDataAuthenticator']] = None,
                 service_url: str = None,
                 service_instance_id: Optional[str] = None) -> None:
        """
        :param service_url: URL of the WOS service eg. https://api.aiopenscale.cloud.ibm.com
        :type service_url: str (required)
        :param service_instance_id: service instance id
        :type service_instance_id: str (required)
        param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        """
        validate_type(authenticator, 'authenticator', [IAMAuthenticator, CloudPakForDataAuthenticator], True)
        self.version = version()
        self.authenticator = authenticator
        self.service_instance_id = service_instance_id
        self.plan_name = None
        self.check_entitlements = False
        super().__init__(authenticator=self.authenticator)

        if authenticator is not None:
            validate_type(service_url, 'service_url', str, False)
            validate_type(service_instance_id, 'service_instance_id', str, False)
            
            if type(authenticator) is IAMAuthenticator:
                self.check_entitlements = True
                
            self.data_marts = DataMarts(self)
            self.service_providers = ServiceProviders(self)
            self.subscriptions = Subscriptions(self)
            self.data_sets = DataSets(self)
            self.monitor_definitions = None
            self.monitor_instances = MonitorInstances(self)
            self.business_applications = BusinessApplications(self)
            
            if service_instance_id is None:
                self.service_instance_id = get_instance_guid(self.authenticator)
                
            if service_url is not None:
                self._generate_service_url(service_url=service_url, instance_id=self.service_instance_id)
            else:
                self._generate_service_url(
                    service_url=WatsonOpenScaleV2Adapter.DEFAULT_SERVICE_URL,
                    instance_id=self.service_instance_id
                )
                
            #Check entitlement for Cloud only
            if self.check_entitlements is True:
                entitlements = EntitlementClient(WatsonOpenScaleV2Adapter.DEFAULT_SERVICE_URL, self.authenticator.token_manager.get_token(), self.service_instance_id)
                self.plan_name = entitlements.is_entitled()

            self.monitor_definitions = MonitorDefinitions(self)

    def _generate_service_url(self, service_url: str = None, instance_id: Optional[str] = None) -> None:
        """
        Generates service url when it is not provided by the user.

        :param str service_url: url to the service (required)
        :param str instance_id: ID of the service instance (optional)
        """
        if instance_id is None and service_url is not None:
            instance_id = get_instance_guid(self.authenticator)
            self.set_service_url("{}/{}".format(service_url, instance_id))
        elif service_url is not None:
            self.set_service_url("{}/{}".format(service_url, instance_id))

    def configure_service(self, *args, **kwargs) -> None:
        """
        Overloaded base method to configure the service (read service_url and store it).
        Additional functionality: dynamically creates additional enums.
        """
        super().configure_service(*args, **kwargs)
        validate_type(self.service_url, 'service_url', str, True)
        instance_id = get_instance_guid(self.authenticator)
        self.set_service_url("{}/{}".format(self.service_url, instance_id))
        self.monitor_definitions = MonitorDefinitions(self)
