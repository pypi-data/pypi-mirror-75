# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import requests

from amazon_ad.api.profiles import Profiles
from amazon_ad.client.base import BaseClient
from amazon_ad.core import exceptions
from amazon_ad.core.utils.amazon import get_endpoint
from amazon_ad.api.report import ReportGet, ReportDownload
from amazon_ad.api.sb.report import SbReport
from amazon_ad.api.sp.report import SpReport


class ZADApiClient(BaseClient):
    API_BASE_URL = 'https://advertising-api-test.amazon.com'

    def __init__(self, client_id,  access_token, profile_id=None, country="US", account_type=None, prepare_mode=False, timeout=None, auto_retry=True, *args, **kwargs):
        super(ZADApiClient, self).__init__(prepare_mode, timeout, auto_retry, *args, **kwargs)
        self.client_id = client_id
        self.access_token = access_token
        self.profile_id = profile_id
        self.country = country
        self.account_type = account_type

    def get_api_base_url(self):
        return get_endpoint(self.country, 'API')

    def _check_request_response(self, response, url, method, **kwargs):
        try:
            response.raise_for_status()
        except requests.Timeout as req_ex:
            self._log_request_error(req_ex, url, method, **kwargs)
            raise exceptions.ZADClientTimeoutException(
                message=None,
                client=self,
                request=req_ex.request,
                response=req_ex.response
            )
        except requests.HTTPError as req_ex:
            self._log_request_error(req_ex, url, method, **kwargs)
            if response.status_code == 401:
                raise exceptions.ZADClientAccessException(
                    message=response.content,
                    client=self,
                    request=req_ex.request,
                    response=req_ex.response
                )

            raise exceptions.ZADClientException(
                message=response.content,
                client=self,
                request=req_ex.request,
                response=req_ex.response
            )
        except requests.RequestException as req_ex:
            self._log_request_error(req_ex, url, method, **kwargs)
            raise exceptions.ZADClientException(
                message=None,
                client=self,
                request=req_ex.request,
                response=req_ex.response
            )

class ZADProfileClient(ZADApiClient):
    profiles = Profiles()

    def __init__(self, client_id,  access_token, country="US", prepare_mode=False, timeout=None, auto_retry=True, *args, **kwargs):
        super(ZADProfileClient, self).__init__(client_id,  access_token, None, country, None, prepare_mode, timeout, auto_retry, *args, **kwargs)

class ZADServiceClient(ZADApiClient):
    report_get = ReportGet()
    report_download = ReportDownload()
    sp_report = SpReport()
    sb_report = SbReport()

    def __init__(self, client_id,  access_token, profile_id, country="US", account_type='seller', prepare_mode=False, timeout=None, auto_retry=True, *args, **kwargs):
        super(ZADServiceClient, self).__init__(client_id,  access_token, profile_id, country, account_type, prepare_mode, timeout, auto_retry, *args, **kwargs)