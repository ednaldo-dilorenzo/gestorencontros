class BusinessException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message
    
    def __repr__(self) -> str:
        return self.message
