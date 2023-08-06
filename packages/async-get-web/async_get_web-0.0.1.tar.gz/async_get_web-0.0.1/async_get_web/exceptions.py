########################################
# exceptions
########################################


class BlaBaseException(Exception):
    pass


class FileURL(BlaBaseException):
    pass


class BadResponse(BlaBaseException):
    pass


class BadContentType(BlaBaseException):
    pass
