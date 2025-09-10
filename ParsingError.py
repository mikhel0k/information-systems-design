class ParsingError(Exception):
    def __init__(self, message, text=None):
        self.message = message
        self.text = text
        if text:
            super().__init__(f"{message}\nТекст: {text}")
        else:
            super().__init__(message)