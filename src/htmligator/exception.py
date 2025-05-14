class TooManyZipFilesError(Exception):

    def __init__(self, message="Too many zip files with the same name"):
        super().__init__(message)
        self.message = message


class PathNotFoundError(Exception):

    def __init__(self, message="Path not found"):
        super().__init__(message)
        self.message = message


class PathIsNotAFolderError(Exception):

    def __init__(self, message="Path is not a folder"):
        super().__init__(message)
        self.message = message
