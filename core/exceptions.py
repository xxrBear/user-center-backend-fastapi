class CustomException(Exception):
    def __init__(self, code: int, description: str) -> None:
        self.code = code
        self.description = description
