#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
try:
    import simplejson as json  # noqa: I900
except ImportError:
    import json


class DatalakeException(Exception):
    def __init__(self, entity=None, params=None, message=None, response=None):
        if not params and not message:
            message = "%s not found" % entity

        self.params = params
        self.message = (
            message or 'entity with params `{}` not found'.format(params)
        )
        self.entity = entity
        self.response = response

        super(DatalakeException, self).__init__(
            self.message, entity,
            params, message
        )

    def __str__(self):
        error = f'\n{self.response.request.method} {self.response.request.url}\n\n'

        try:
            error += (
                f'{json.dumps(self.response.json(), indent=4)}'
            )

        except json.JSONDecodeError:
            error += (
                f'{self.response.text}'
            )


        try:
            request_id = self.response.request.headers.get(
                'X-Request-ID', 'unknown'
            )

            error += (
                f'\nProvided request_id: {request_id}\n'
            )
        except Exception:
            error += (
                f'\nProvided request_id: Unknown\n'
            )

        return error


class DatalakePayloadTooLargeException(DatalakeException):

    def __str__(self):
        error = super().__str__()
        if self.response.status_code == 413:
            error += (
                '\nA file you are attempting to pass is probably too large for our server.'
                ' If passing a sample_data file please make sure it is under 10 Megabytes.\n\n'
            )

        return error


class DataframeStreamingException(DatalakeException):

    def __init__(self, error, url, entity=None, params=None, message=None,
                 response=None):
        self.url = url
        self.error = error
        super().__init__(
            entity=entity,
            params=params,
            message=message,
            response=response
        )

    def __str__(self):
        msg = json.dumps(self.error, indent=4)
        return f'\n A GET request was made to the following url: ' \
               f'{self.url}\n\n{msg}'


class TimeoutException(DatalakeException):
    pass


class CatalogueEntityNotFoundException(DatalakeException):
    pass


class InvalidPayloadException(DatalakeException):
    pass


class UnAuthorisedAccessException(DatalakeException):
    pass


class DatalakeGatewayTimeout(DatalakeException):
    message = (
        'This request to the Datalake has timed-out. This means that the '
        'request required too much processing. Please report this error '
        'to a member of the Datalake support team.'
    )


class DatalakeServiceUnavailable(DatalakeException):
    message = (
        'IHS Markit datalake is unavailable. Please try again in a few seconds.'
    )


class InsufficientPrivilegesException(DatalakeException):
    message = 'Insufficient privileges to perform this action'


class S3FileDoesNotExist(DatalakeException):
    def __init__(self, file_path):
        self.message = (
            "Either file at path `%s` does not exist / Potential issue with the bucket policy."
            "Please reach out to Datalake Tech Data Ops user for resolution." % file_path
        )

        super(S3FileDoesNotExist, self).__init__(self.message)


class DownloadFailed(DatalakeException):
    pass


class NoAccountSpecified(DatalakeException):

    def __init__(self, accounts):
        self.accounts = accounts
        self.message = (
            "Unable to default the account for access_manager_id, tech_data_ops_id and/or manager_id "
            "due to multiple accounts being attached to this API key. "
            "Your accounts are: %s" % [(a.id, a.name) for a in accounts]
        )
        super(NoAccountSpecified, self).__init__(self.message)


class AuthenticationFailure(Exception):
    """
    An exception wrapping an authentication failure response. If the response
    had a payload, that payload is reported as the exception message, otherwise
    a generic error message is returned.
    """
    GENERIC_ERROR_MESSAGE = (
        'API key is not valid or has expired.'
        ' Please generate a new key in the Catalogue UI and try again.'
    )

    def __init__(self, response=None, message=None):
        self.response = response
        self.message = message

    def __str__(self):
        if self.response and self.response.text:
            return self.response.text
        elif self.message:
            return self.message
        return self.GENERIC_ERROR_MESSAGE
