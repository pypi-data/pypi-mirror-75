# -*- coding: utf-8 -*-
__author__ = 'vivian'

import yaml
from dss_python_sdk.http_utils import http_get


TIMEOUT = 3
PROFILE_RC1 = "rc1"
PROFILE_RC2 = "rc2"
PROFILE_PROD = "prod"


def get_db_properties(url, plat_key, svc_code, profile, user_agent):
    """
    Get database connection parameters
    :param url:
    :param plat_key:
    :param svc_code:
    :param profile:
    :param user_agent:
    :return:
    """
    if url is None or url.strip() == "":
        raise Exception("URL can't be empty string")
    if not url.startswith("https"):
        raise Exception("Only https protocol is supported ")
    if plat_key is None or plat_key.strip() == "":
        raise Exception("plat_key can't be empty string")
    if svc_code is None or svc_code.strip() == "":
        raise Exception("svc_code can't be empty string")
    if profile is None or profile.strip() == "":
        raise Exception("profile can't be empty string")
    if profile != PROFILE_RC1 and profile != PROFILE_RC2 and profile != PROFILE_PROD:
        raise Exception("profile error")
    prams = {"platkey": plat_key, "svccode": svc_code, "profile": profile}
    if user_agent.strip() == "":
        user_agent = svc_code
    res_bytes = http_get(url, user_agent, prams, TIMEOUT)
    d = yaml.load(res_bytes, Loader=yaml.FullLoader)
    try:
        ret_dict = d["database"]
        return ret_dict
    except TypeError:
        # It indicates that the server does not return db.yml file normally, either the PLATKEY is wrong,
        # or the SVCCODE is wrong, or the PROFILE is wrong.
        # If there is no problem in self-examination, contact the data source management system administrator
        raise Exception(res_bytes)
