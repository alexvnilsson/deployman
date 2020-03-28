class ReadManifestError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)

        if errors is not None:
            self.errors = errors