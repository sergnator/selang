class Token:
    def __init__(self, token_type, text):
        self.token_type = token_type
        self.text = text

    def __str__(self):
        return f"{self.text} : {self.token_type}"

    def __repr__(self):
        return self.__str__()