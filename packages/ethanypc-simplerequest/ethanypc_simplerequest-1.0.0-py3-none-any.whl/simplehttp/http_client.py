import sys
import http.client
import json
from simplehttp.utils import process_url
from simplehttp.error import HttpError
from urllib.parse import urlencode


def make_request(method, url, params={}, data={}):
    url_parts = process_url(url, params)
    conn = http.client.HTTPSConnection(url_parts['host'])
    if (method == 'GET'):
        conn.request('GET', url_parts['path'])
    elif (method == 'POST'):
        headers = {'Content-Type': "application/json"}
        conn.request('POST', url_parts['path'],
                     body=json.dumps(data), headers=headers)
    response = conn.getresponse()
    status = str(response.status)
    if not status.startswith('2'):
        raise HttpError(f"HTTP Status Code: {status}", int(status))
    # body here is byte string.
    body = response.read()
    return json.loads(body)


def get_json(url, params={}):
    try:
        body = make_request('GET', url, params)
    except Exception as e:
        sys.last_value = e
        # re-raise the exception (allow the caller to handle)
        raise
    return body


def post_json(url, params={}, data={}):
    try:
        body = make_request('POST', url, params, data)
    except Exception as e:
        sys.last_value = e
        raise
    return body

# def post_json(url, params={}, data={}):
#     url_parts = process_url(url, params)
#     conn = http.client.HTTPSConnection(url_parts['host'])
#     headers = {'Content-Type': "application/json"}
#     conn.request('POST', url_parts['path'],
#                  body=json.dumps(data), headers=headers)
#     response = conn.getresponse()
#     status = str(response.status)
#     if not status.startswith('2'):
#         raise simplehttp.HttpError(f"HTTP Status Code: {status}", status)
#     body = response.read()
#     return json.loads(body)
