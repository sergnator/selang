import re

from Tokens.Token import Token
from Tokens.TokenType import TokenType, TokenTypes


class Lang:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []

    def lex_analytic(self):
        while self.__next():
            pass
        return self.tokens

    def __next(self):
        for type_ in list(TokenTypes.values()):
            if self.pos >= len(self.code):
                return False

            regex = re.match(type_.regex, self.code[self.pos:])
            if regex:
                self.tokens.append(Token(type_, regex.group()))
                self.pos += len(regex.group())
                return True
        raise SyntaxError(f'{self.code[self.pos:].split()[0]} syntax error on position {self.pos + 1}')