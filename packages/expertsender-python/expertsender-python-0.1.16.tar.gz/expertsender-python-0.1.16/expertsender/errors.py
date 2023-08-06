class Error(Exception):
    """Base class for other exceptions."""
    pass


class ExpertsenderError(Error):
    """Generic Return Error."""
    pass


class ExpertsenderExportError(Error):
    """Error regarding the export of users"""
    pass


class ExpertsenderImportError(Error):
    """Error regarding the export of users"""
    pass
