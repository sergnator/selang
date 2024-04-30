from _ast import BinOp

from nodes.RootNode import *
from Tokens.TokenType import *


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.scope = {}
        self.pos = 0

    def run(self, node):
        if isinstance(node, RootNode):
            for node_ in node.code_string:
                self.run(node_)
            return
        if isinstance(node, VariableNode):
            try:
                return self.scope[f"{node.var.text}"]
            except KeyError:
                raise SyntaxError(f"Variable {node.var.text} is not defined")
        if isinstance(node, BinOperand):
            if node.operator.token_type.name == "EQUALS":
                result = self.run(node.right)
                self.scope[f"{node.left.var.text}"] = result
                return result
            if node.operator.token_type.name == "PLUS":
                return self.run(node.left) + self.run(node.right)
            if node.operator.token_type.name == "MINUS":
                return self.run(node.left) - self.run(node.right)
            if node.operator.token_type.name == "LOGICAL":
                if node.operator.text == "==":
                    return self.run(node.left) == self.run(node.right)
                if node.operator.text == "!=":
                    return self.run(node.left) != self.run(node.right)
                if node.operator.text == "<":
                    return self.run(node.left) < self.run(node.right)
                if node.operator.text == ">":
                    return self.run(node.left) > self.run(node.right)
        if isinstance(node, UnaryOperand):
            if node.operator.token_type.name == "PRINT":
                print(self.run(node.operand))
            if node.operator.token_type.name == "IF":
                if self.run(node.operand):
                    self.run(node.body)
            if node.operator.token_type.name == "WHILE":
                while self.run(node.operand):
                    self.run(node.body)
        if isinstance(node, NumNode):
            return int(node.num.text)
        if isinstance(node, BooleanNode):
            if node.value.text == "True":
                return True
            return False

    def parse(self):
        root = RootNode()
        while self.pos < len(self.tokens):
            line_code = self.__parse_line()
            if self.__math(TokenTypes["END"]) is None:
                raise SyntaxError("Unexpected end of line ;")
            root.add_node(line_code)
        return root

    def __math(self, token_type: TokenType):
        if self.pos < len(self.tokens):
            while self.tokens[self.pos].token_type.name == "SPACE":
                self.pos += 1
            current_token = self.tokens[self.pos]
            if token_type.name == current_token.token_type.name:
                self.pos += 1
                return current_token
        return None

    def __current_token(self):
        if self.pos < len(self.tokens):
            while self.tokens[self.pos].token_type.name == "SPACE":
                self.pos += 1
            current_token = self.tokens[self.pos]
            return current_token
        return None

    def __parse_line(self):
        var = self.__math(TokenTypes["VAR"])
        if var is None:
            print_token = self.__math(TokenTypes["PRINT"])
            if print_token is None:
                token_with_body = self.__math(TokenTypes["IF"])
                if token_with_body is None:
                    token_with_body = self.__math(TokenTypes["WHILE"])
                if token_with_body is None:
                    raise SyntaxError("Неизвестный синтаксис")
            if self.__math(TokenTypes["START BRACKET"]) is None:
                raise SyntaxError("Ожидалось открытие скобки")
            right = self.__parse_formula()
            if self.__math(TokenTypes["END BRACKET"]) is None:
                raise SyntaxError("Скобка никогда не закрывается")
            if print_token is not None:
                return UnaryOperand(print_token, right)
            if self.__math(TokenTypes["START NAME SPACE"]) is None:
                raise SyntaxError("Тело условного оператора обязательно")
            body_operator = self.__parse_name_space()
            return NodeWBody(token_with_body, right, body_operator)

        var = self.__parse_num_or_var_or_bool()
        eq = self.__math(TokenTypes["EQUALS"])
        if eq is not None:
            right = self.__parse_formula()
            binary_operand = BinOperand(eq, var, right)
            return binary_operand
        raise SyntaxError("Ожидался оператор присваивания")

    def __parse_num_or_var_or_bool(self):
        num = self.__math(TokenTypes["NUM"])
        if num is not None:
            return NumNode(num)
        var = self.__math(TokenTypes["NAME VAR"])
        if var is not None:
            return VariableNode(var)
        bool_ = self.__math(TokenTypes["BOOL"])
        if bool_ is not None:
            return BooleanNode(bool_)
        raise SyntaxError("Неверный синтаксис ожидалось число или имя переменной")

    def __parse_formula(self):
        left = self.__parse_num_or_var_or_bool()
        operator = self.__math(TokenTypes["PLUS"])
        if operator is None:
            operator = self.__math(TokenTypes["MINUS"])
        if operator is None:
            operator = self.__math(TokenTypes["LOGICAL"])
        node_formula = left
        while operator is not None:
            right = self.__parse_num_or_var_or_bool()
            node_formula = BinOperand(operator, left, right)
            operator = self.__math(TokenTypes["PLUS"])
            if operator is None:
                operator = self.__math(TokenTypes["MINUS"])
        return node_formula

    def __parse_name_space(self):
        root = RootNode()
        while self.__math(TokenTypes["END NAME SPACE"]) is None:
            if self.pos >= len(self.tokens):
                raise SyntaxError("Brake { never closed")
            line = self.__parse_line()
            if self.__math(TokenTypes["END"]) is None:
                raise SyntaxError("Unexpected end of line ;")
            root.add_node(line)
        return root
