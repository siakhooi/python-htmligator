class TooManyZipFilesError(Exception):

    def __init__(
        self,
        message: str = (
            "Too many zip files with the same name"
        ),
    ) -> None:
        super().__init__(message)
        self.message: str = message


class PathNotFoundError(Exception):

    def __init__(self, message: str = "Path not found") -> None:
        super().__init__(message)
        self.message: str = message


class PathIsNotAFolderError(Exception):

    def __init__(self, message: str = "Path is not a folder") -> None:
        super().__init__(message)
        self.message: str = message
