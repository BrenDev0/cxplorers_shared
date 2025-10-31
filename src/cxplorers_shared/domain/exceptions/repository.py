class RepositoryError(Exception):
    def __init__(self, detail: str = "Error in repository operations"):
        super().__init__(detail)