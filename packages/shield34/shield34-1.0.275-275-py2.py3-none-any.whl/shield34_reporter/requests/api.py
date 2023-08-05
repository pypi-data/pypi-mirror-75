import requests
import httpx
from shield34_reporter.utils.external_proxy import get_external_proxies
from shield34_reporter.consts.shield34_properties import Shield34Properties


def request(method, url, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.request(method=method,
                                    url=url,
                                    **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.request(method=method,
                                      url=url,
                                      data=get_arg('data', None, **kwargs),
                                      files=get_arg('files', None, **kwargs),
                                      json=get_arg('json', None, **kwargs),
                                      params=get_arg('params', None, **kwargs),
                                      headers=get_arg('headers', None, **kwargs),
                                      cookies=get_arg('cookies', None, **kwargs),
                                      auth=get_arg('auth', None, **kwargs),
                                      allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                      timeout=get_arg('timeout', 30, **kwargs)
                                      )
            return response


def get(url, params=None, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.get(url=url,
                                params=params,
                                **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.get(url=url,
                                  params=params,
                                  headers=get_arg('headers', None, **kwargs),
                                  cookies=get_arg('cookies', None, **kwargs),
                                  auth=get_arg('auth', None, **kwargs),
                                  allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                  timeout=get_arg('timeout', 30, **kwargs)
                                  )
            return response


def post(url, data=None, json=None, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.post(url=url,
                                 data=data,
                                 json=json,
                                 **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.post(url=url,
                                   data=data,
                                   json=json,
                                   files=get_arg('files', None, **kwargs),
                                   params=get_arg('params', None, **kwargs),
                                   headers=get_arg('headers', None, **kwargs),
                                   cookies=get_arg('cookies', None, **kwargs),
                                   auth=get_arg('auth', None, **kwargs),
                                   allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                   timeout=get_arg('timeout', 30, **kwargs)
                                   )
            return response


def options(url, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.options(url, proxies=get_external_proxies(), **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.options(url=url,
                                      params=get_arg('params', None, **kwargs),
                                      headers=get_arg('headers', None, **kwargs),
                                      cookies=get_arg('cookies', None, **kwargs),
                                      auth=get_arg('auth', None, **kwargs),
                                      allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                      timeout=get_arg('timeout', 30, **kwargs)
                                      )
            return response


def head(url, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.head(url, proxies=get_external_proxies(), **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.head(url=url,
                                   params=get_arg('params', None, **kwargs),
                                   headers=get_arg('headers', None, **kwargs),
                                   cookies=get_arg('cookies', None, **kwargs),
                                   auth=get_arg('auth', None, **kwargs),
                                   allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                   timeout=get_arg('timeout', 30, **kwargs)
                                   )
            return response


def put(url, data=None, **kwargs):
    if Shield34Properties.http_library == 'requests':
        response = requests.put(url=url,
                                data=data,
                                **kwargs)
        return response
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.put(url=url,
                                  data=get_arg('data', None, **kwargs),
                                  files=get_arg('files', None, **kwargs),
                                  json=get_arg('json', None, **kwargs),
                                  params=get_arg('params', None, **kwargs),
                                  headers=get_arg('headers', None, **kwargs),
                                  cookies=get_arg('cookies', None, **kwargs),
                                  auth=get_arg('auth', None, **kwargs),
                                  allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                  timeout=get_arg('timeout', 30, **kwargs)
                                  )
            return response


def patch(url, data=None, **kwargs):
    if Shield34Properties.http_library == 'requests':
        return requests.patch(url, data=data, proxies=get_external_proxies(), **kwargs)
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.patch(url=url,
                                    data=get_arg('data', None, **kwargs),
                                    files=get_arg('files', None, **kwargs),
                                    json=get_arg('json', None, **kwargs),
                                    params=get_arg('params', None, **kwargs),
                                    headers=get_arg('headers', None, **kwargs),
                                    cookies=get_arg('cookies', None, **kwargs),
                                    auth=get_arg('auth', None, **kwargs),
                                    allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                    timeout=get_arg('timeout', 30, **kwargs)
                                    )
            return response


def delete(url, **kwargs):
    if Shield34Properties.http_library == 'requests':
        return requests.delete(url, proxies=get_external_proxies(), **kwargs)
    if Shield34Properties.http_library == 'httpx':
        with httpx.Client(verify=Shield34Properties.enable_ssl_certificate_verification,
                          proxies=get_external_proxies()) as client:
            response = client.delete(url=url,
                                     params=get_arg('params', None, **kwargs),
                                     headers=get_arg('headers', None, **kwargs),
                                     cookies=get_arg('cookies', None, **kwargs),
                                     auth=get_arg('auth', None, **kwargs),
                                     allow_redirects=get_arg('allow_redirects', True, **kwargs),
                                     timeout=get_arg('timeout', 30, **kwargs)
                                     )
            return response


def get_arg(name, default_value, **kwargs):
    if name in kwargs:
        return kwargs.get(name)
    else:
        return default_value
