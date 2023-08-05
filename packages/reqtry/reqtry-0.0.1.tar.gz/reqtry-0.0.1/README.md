# reqtry

A simple implementation of retries for [psf/request](https://github.com/psf/requests) python library. Retry code is based in retry project [invl/retry](https://github.com/invl/retry)

It has the same functions of request/api.py only retries functionality was added. (request, get, post, put, patch, delete, options, head)

## Installation

```bash
    $ pip install reqry
```

## Api

### Request

```python
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
        :returns: the result of the f function."""
```

### Get

```python
    def get(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Post

```python
    def post(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Put

```python
    def put(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Patch

```python
    def patch(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Delete

```python
    def delete(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Options

```python
    def options(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

### Head

```python
    def head(url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None, tries=1, delay=0, max_delay=None, backoff=1, jitter=0,
            logger=logging_logger, raise_for_status=True)
```

## Examples

```python
    import reqtry

    reqtry.get(url, cookies=self._cookies, timeout=(3, 3), tries=3, delay=1)
        '''Raise error after 3 attempts, sleep 1 seconds between attempts.'''

    reqtry.get(url, cookies=self._cookies, timeout=(3, 3), delay=1, backoff=2, max_delay=8)
        '''Raise error after 3 attempts, sleep 1, 2, 4 and 8 seconds between attempts.'''

    reqtry.get(url, cookies=self._cookies, timeout=(3, 3), delay=1, max_delay=4, jitter=1)
        '''Raise error after 3 attempts, sleep 1, 2, 3 and 4 seconds between attempts.'''
```
