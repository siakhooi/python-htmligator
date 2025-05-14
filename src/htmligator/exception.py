class TooManyZipFilesError(Exception):

    def __init__(self, message="Too many zip files with the same name"):
        super().__init__(message)
        self.message = message
