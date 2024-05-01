from nodes.RootNode import *
from Parser.Le import *


class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.scope = {}
        self.pos = 0

    def run(self, node):
        if isinstance(node, RootNode):
            res = []
            for node_ in node.code_string:
                res.append(self.run(node_))
                return res
            return
        if isinstance(node, FunctionNode):
            try:
                function_form_scope = self.scope[node.obj.text]
            except KeyError:
                raise SyntaxError(f"Function {node.obj.text} is not defined")
            if not isinstance(function_form_scope, tuple):
                raise SyntaxError(f"Obj {node.obj.text} is not callable")
            return function_form_scope[1](*self.run(node.params))
        if isinstance(node, ObjNode):
            try:
                return self.scope[f"{node.obj.text}"]
            except KeyError:
                raise SyntaxError(f"Variable {node.obj.text} is not defined")
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
        if isinstance(node, StringNode):
            text: str = node.value.text
            return text[1:-1]

    def parse(self):
        root = RootNode()
        self.scope["input"] = ([], input)
        self.scope["print"] = (["text"], print)
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

    def __parse_name(self):
        name = self.__math(TokenTypes["OBJ"])
        if name is None:
            raise SyntaxError(f"Ожидался индификатор")

    def __parse_var(self):
        var = self.__parse_name()
        eq = self.__math(TokenTypes["EQUALS"])
        if eq is not None:
            right = self.__parse_formula()
            binary_operand = BinOperand(eq, var, right)
            return binary_operand
        raise SyntaxError("Ожидалось =")

    def __parse_line(self):
        var = self.__math(TokenTypes["VAR"])
        if var is not None:
            return self.__parse_var()
        obj = self.__math(TokenTypes["OBJ"])
        if obj is not None:
            params = self.__math(TokenTypes["PARAMS"])
            if params is not None:
                return FunctionNode(obj, self.__parse_params(params))

    def __parse_variable_a(self, obj):
        eq = self.__math(TokenTypes["EQUALS"])
        if eq is not None:
            right = self.__parse_formula()
            binary_operand = BinOperand(eq, eq, right)
            return binary_operand
        raise SyntaxError("Ожидалось =")

    def __parse_body_function(self):
        if self.__math(TokenTypes["START NAME SPACE"]) is not None:
            root = RootNode()
            while self.pos < len(self.tokens):
                line_code = self.__parse_line()
                if self.__math(TokenTypes["END"]) is None:
                    raise SyntaxError("Unexpected end of line ;")
                root.add_node(line_code)
            if self.__math(TokenTypes["END NAME SPACE"]) is not None:
                return root
            raise SyntaxError("{ never closed")
        raise SyntaxError("Ожидалось {")

    def __parse_params(self, params):
        params = params.text.split("(")[-1].split(")")[0].split(',')
        root = RootNode()
        for param in params:
            lang = Lang(param)
            tokens = lang.lex_analytic()
            tokens_without_space = []
            for token in tokens:
                if token.token_type.name != "SPACE":
                    tokens_without_space.append(token)
            tokens = tokens_without_space[:]
            for i in range(len(tokens)):
                if tokens[i].token_type.name == "NUM" or tokens[i].token_type.name == "BOOL" or tokens[
                    i].token_type.name == "STRING":
                    num = NumNode(tokens[i])
                    if i == len(tokens) - 1:
                        root.add_node(num)
                        break
                    operator = tokens[i + 1]
                    while operator.token_type.name == "PLUS" or operator.token_type.name == "MINUS" or operator.token_type.name == "LOGICAL":
                        left = tokens[tokens.index(operator) + 1]
                        left_node = NumNode(left)

                        num = BinOperand(operator, num, left_node)
                        if tokens.index(left) == len(tokens) - 1:
                            break
                        operator = tokens[tokens.index(left) + 1]
                    root.add_node(num)
                if tokens[i].token_type.name == "OBJ":
                    root.add_node(ObjNode(tokens[i]))
        return root

    def __parse_num_or_var_or_bool_str(self):
        num = self.__math(TokenTypes["NUM"])
        if num is not None:
            return NumNode(num)
        var = self.__math(TokenTypes["OBJ"])
        if var is not None:
            return CreateVariableNode(var)
        bool_ = self.__math(TokenTypes["BOOL"])
        if bool_ is not None:
            return BooleanNode(bool_)
        str_ = self.__math(TokenTypes["STRING"])
        if str_ is not None:
            return StringNode(str_)
        raise SyntaxError("Неверный синтаксис ожидалось число или имя переменной")

    def __parse_formula(self):
        left = self.__parse_num_or_var_or_bool_str()
        operator = self.__math(TokenTypes["PLUS"])
        if operator is None:
            operator = self.__math(TokenTypes["MINUS"])
        if operator is None:
            operator = self.__math(TokenTypes["LOGICAL"])
        node_formula = left
        while operator is not None:
            right = self.__parse_num_or_var_or_bool_str()
            node_formula = BinOperand(operator, node_formula, right)
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
