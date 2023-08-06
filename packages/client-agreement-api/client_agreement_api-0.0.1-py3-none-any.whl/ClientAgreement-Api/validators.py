import logging

from connexion import decorators

logger = logging.getLogger("connexion.decorators.validation")


class RequestBodyValidator(decorators.validation.RequestBodyValidator):
    """
    This class overrides the default connexion RequestBodyValidator
    so that it returns the complete string representation of the
    error, rather than just returning the error message.

    For more information:
        - https://github.com/zalando/connexion/issues/558
        - https://connexion.readthedocs.io/en/latest/request.html
    """

    def validate_schema(self, data, url):
        return super(RequestBodyValidator, self).validate_schema(data, url)
