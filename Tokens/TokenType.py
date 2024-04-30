class TokenType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def __str__(self):
        return self.name


TokenTypes = {
    "IF": TokenType("IF", r"if"),
    "WHILE": TokenType("WHILE", r"while"),
    "BOOL": TokenType("BOOL", r"True|False"),
    "LOGICAL": TokenType("LOGICAL", r"<|>|==|!="),
    "VAR": TokenType("VAR", "var"),
    "SPACE": TokenType("SPACE", r"\s"),
    "END": TokenType("END", ";"),
    "PLUS": TokenType("PLUS", "[+]"),
    "MINUS": TokenType("MINUS", "-"),
    "NUM": TokenType("NUM", "[0-9]+"),
    "PRINT": TokenType("PRINT", "print"),
    "EQUALS": TokenType("EQUALS", "={1}?"),
    "NAME VAR": TokenType("NAME VAR", r"(([a-z])|([A-z]))+"),
    "START NAME SPACE": TokenType("START NAME SPACE", r"[{]"),
    "END NAME SPACE": TokenType("END NAME SPACE", r"[}]"),
    "START BRACKET": TokenType("START BRACKET", r"[(]"),
    "END BRACKET": TokenType("END BRACKET", r"[)]")}
