class HackDBException(Exception):
    pass

class HackDBSiteKeyException(HackDBException):
    pass

class HackDBOriginException(HackDBException):
    pass

class HackDBProjectException(HackDBException):
    pass

class HackDBCollectionNotFoundException(HackDBException):
    pass

class HackDBUnauthenticatedException(HackDBException):
    pass

def _get_exception(code: str):
    match code:
        case "origin_required":
            pass
        case "origin_not_allowed":
            return HackDBOriginException
        case "invalid_site_key":
            pass
        case "missing_site_key":
            return HackDBSiteKeyException
        case "no_project":
            return HackDBProjectException
        case "collection_not_found":
            return HackDBCollectionNotFoundException
    return HackDBException

