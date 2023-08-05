def handle_status_code(func):
    """ Decorator to handle http errors from requests lib.

    Arguments:
        func {[type]} -- Function which include requests func and response.raise_for_status()

        https://github.com/psf/requests/blob/2758124a13cddff7244b97b5ffe3fddabb90bc18/requests/status_codes.py

    Raises:
        Exception: Exception being raised in response.raise_for_status() will be raised in hycli.

    Returns:
        [type] -- [description]
    """

    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if not err.response:
                raise Exception(err)
            elif err.response.status_code == 401:
                raise Exception("API credentials not correct.")
            else:
                raise Exception(
                    f"{err}\n Response: {str(err.response._content, 'utf-8')}"
                )

    return decorator
