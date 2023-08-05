import os
import json
import logging
from urllib.parse import urljoin
from base64 import urlsafe_b64decode
import requests

GCP_PROJECT = os.environ["GCP_PROJECT"]
FUNCTION_REGION = os.environ["FUNCTION_REGION"]


class ServiceError(Exception):
    def __init__(self, status_code, message):
        if status_code >= 500:
            logging.error(message)
        else:
            logging.warning(message)
        super().__init__(message)


def get_auth_header(audience):
    if os.getenv("LOCAL"):
        from subprocess import Popen, PIPE

        token = (
            Popen(["gcloud", "auth", "print-identity-token"], stdout=PIPE)
            .communicate()[0][:-1]
            .decode()
        )
        return {"Authorization": "Bearer " + token}
    token_url = (
        "http://metadata.google.internal"
        "/computeMetadata/v1/instance/service-accounts/default/identity"
        f"?audience={audience}"
    )
    token = requests.get(
        url=token_url, headers={"Metadata-Flavor": "Google"},
    ).content.decode()
    return {"Authorization": "Bearer " + token}


def call(name, **kwargs):
    domain = f"https://{FUNCTION_REGION}-{GCP_PROJECT}.cloudfunctions.net"
    url = urljoin(domain, name)
    logging.info("CALL: %s", name)
    logging.info(kwargs)
    r = requests.post(url, headers=get_auth_header(url), json=kwargs)
    resp = r.json()
    logging.info("RESPONSE: %s", name)
    logging.info(resp)
    r.raise_for_status()
    return resp


def user_info(request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return None
