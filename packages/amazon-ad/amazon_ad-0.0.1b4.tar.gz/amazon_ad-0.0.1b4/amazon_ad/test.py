# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import requests

from client.service import ZADServiceClient, ZADProfileClient
from client.auth import ZADAuthClient

client_id = 'amzn1.application-oa2-client.5f22ade077114ef980883e2045a2fde0'
client_secret = '1ac684981fd46f98752ac47929606cb1587a42ed1045de7f10a2391fd498769d'

access_token = 'Atza|IwEBIAJs-7MfC22k8FpsPglkqCdNm9xcOPH566mBdjS2gpZMTVHCISqs_3t_S05JObNl07EIaox4ZDMNeBbPcxRd9DybJM_lX7jw86RWbl3c0JsBCFSBjt6FTEPuQC-fCOUwOPvMqfj1thstV-Q91JoEzt6fcwpabKTNUx00Bs1EX2Fxu1_cUd6Ypl_AEdhkQOZnIDGpqqr2x8El8Sz-h6BpGFOsMFlMTBUGZhKppKUxL6zDQCES_uAyypI8W0wqsRGIR6goSxDp06qQDiIv7O5onVqmHMDz4exOq1QbNCwgl62ML3NySGuGYb4stRy-YUZLlprkoIoNui9717w5eb12GsbhzRQEEen8PpQCO9Ov4ylaBXjKPWacPlnUC92IuwdUoEl-0yWp9bzMLYmaSSoSP-hvM9Ab80GiTWa7s5exa8p6ybMHtyGQfGRivvBtU3XMqgk'

def auth():
    auth_client = ZADAuthClient(client_id, client_secret, 'SANDBOX')
    url = auth_client.authorization_url('http://localhost/', '{"xixi":"haha"}')
    print(url)

def refresh_access_token():
    refresh_token = 'Atzr|IwEBIAqVizlqGLRyEYDrjc4Nj7jQxbPh7yUvXxt7Kal0cXGgpKCk_cs93eMFeHdZgRNmtm1cimC4as6LEw4wJgIClRboOQ9bTL4ACkdnGoj50FZmW89EO9dQI41iH3iOkfObZTC8kyHowmwlj2ETKkGdXXeIunJj8u7FF_o44VbITAXybUuIJIN6k3cuvb2MSxxpOgdtUeRG-nmxV9e9ouIEopYK1M4gI4oH1gLadX_5AURiJDUcudDmY_nGu7fAvi8jhRsarjz4Y7fTCSm2Ijkk10uzHixHMJC7Qjqrh-7soJ0VLkoyO27gcDLzL4DWNyUpaaPvPeoAyAEvQUr-QYY1uVPEXhbOeGSVqXcegFJDMcEpl_w1HqqZPNAjAD9LTBkHvkACg8LwWfMzuh3WpAi0Hmo6SdbrKA2r7mrmZC3lH2YQQg'
    auth_client = ZADAuthClient(client_id, client_secret, 'SANDBOX')
    res = auth_client.token.refresh_token(refresh_token)
    print(res)

def profile():
    client = ZADProfileClient(client_id, access_token, country="SANDBOX")
    a = client.profiles.list()
    print(a)

def test():

    # client = ZADServiceClient(client_id, access_token, country="SANDBOX")
    # a = client.profiles.retrieve('4358504360586791')
    # print(a)

    client = ZADServiceClient(client_id, access_token, profile_id='4358504360586791', country="SANDBOX", prepare_mode=True)
    # a = client.sb_report.queries('20200720')
    # a = client.report_get.get_report('amzn1.clicksAPI.v1.m1.5F18F3C3.b2fffb10-7796-46ef-bbee-654c94a84717')
    a = client.report_download.download_report('https://advertising-api-test.amazon.com/v1/reports/amzn1.clicksAPI.v1.m1.5F18F3C3.b2fffb10-7796-46ef-bbee-654c94a84717/download')

    print(a)

test()