class MissingRequiredConfiguration(Exception):
    pass


class IncorrectTypePermissionConfiguration(Exception):
    pass


class ApplicationSettingsNotFound(Exception):
    """
    Exception that indicates the application settings was not found through known methods.
    """


class RequestIDModuleNotFound(Exception):
    """
    Exception that indicates the request id module was not found through known methods.
    """
