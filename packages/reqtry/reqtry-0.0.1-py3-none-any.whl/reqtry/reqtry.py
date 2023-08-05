import requests
import logging
import random
import time

logging_logger = logging.getLogger(__name__)


def request(method, url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True):
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.request('GET', 'https://httpbin.org/get')
      >>> r
      <Response [200]>
    """

    _tries, _delay = tries, delay
    while _tries:
        try:
            with requests.sessions.Session() as session:
                if raise_for_status:
                    r = session.request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                                        auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                                        hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
                    r.raise_for_status()
                    return r
                else:
                    return session.request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                                           auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                                           hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        except Exception as e:
            _tries -= 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning('%s, retrying in %s seconds...', e, _delay)

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)


def get(url, params=None, data=None, headers=None, cookies=None, files=None,
        auth=None, timeout=None, allow_redirects=True, proxies=None,
        hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
        logger=logging_logger, raise_for_status=True):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable GET redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.get('https://httpbin.org/get')
      >>> r
      <Response [200]>
    """

    return request('get', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def post(url, params=None, data=None, headers=None, cookies=None, files=None,
         auth=None, timeout=None, allow_redirects=True, proxies=None,
         hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
         logger=logging_logger, raise_for_status=True):
    r"""Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable POST redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.post('https://httpbin.org/post')
      >>> r
      <Response [200]>
    """

    return request('post', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def put(url, params=None, data=None, headers=None, cookies=None, files=None,
        auth=None, timeout=None, allow_redirects=True, proxies=None,
        hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
        logger=logging_logger, raise_for_status=True):
    r"""Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable PUT redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.put('https://httpbin.org/put')
      >>> r
      <Response [200]>
    """

    return request('put', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def patch(url, params=None, data=None, headers=None, cookies=None, files=None,
          auth=None, timeout=None, allow_redirects=True, proxies=None,
          hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
          logger=logging_logger, raise_for_status=True):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable PATCH redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.patch('https://httpbin.org/patch')
      >>> r
      <Response [200]>
    """

    return request('patch', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def delete(url, params=None, data=None, headers=None, cookies=None, files=None,
           auth=None, timeout=None, allow_redirects=True, proxies=None,
           hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
           logger=logging_logger, raise_for_status=True):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable DELETE redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.delete('https://httpbin.org/delete')
      >>> r
      <Response [200]>
    """

    return request('delete', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def options(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable OPTIONS redirection. Defaults to ``True``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.options('https://httpbin.org/options')
      >>> r
      <Response [200]>
    """

    return request('options', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)


def head(url, params=None, data=None, headers=None, cookies=None, files=None,
         auth=None, timeout=None, allow_redirects=False, proxies=None,
         hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
         logger=logging_logger, raise_for_status=True):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :type timeout: float or tuple
    :param allow_redirects: (optional) Boolean. Enable/disable HEAD redirection. Defaults to ``False``.
    :type allow_redirects: bool
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    Executes a request and retries it if it failed.

    :param tries: the maximum number of attempts. default: 1.
    :param delay: initial delay between attempts. default: 0.
    :param max_delay: the maximum value of delay. default: None (no limit).
    :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
    :param jitter: extra seconds added to delay between attempts. default: 0.
                   fixed if a number, random if a range tuple (min, max)
    :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                   default: retry.logging_logger. if None, logging is disabled.
    :param rise_for_status: (optional) Boolean. Enable/disable rise an error when the response HTTP status code
                            is a 4xx or a 5xx. Defaults to ``True``.
    :returns: the result of the f function.

    Usage::

      >>> from marcotools import req
      >>> r = req.head('https://httpbin.org/head')
      >>> r
      <Response [200]>
    """

    return request('head', url, params=params, data=data, headers=headers, cookies=cookies, files=files,
                   auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                   hooks=hooks, stream=stream, verify=verify, cert=cert, json=json, tries=tries, delay=delay, max_delay=max_delay, backoff=backoff, jitter=jitter,
                   logger=logger, raise_for_status=raise_for_status)
