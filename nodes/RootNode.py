from Tokens.Token import Token


class Node:
    def __init__(self):
        self.code_string = []


class RootNode(Node):
    def add_node(self, node: Node):
        self.code_string.append(node)


class BinOperand(Node):
    def __init__(self, operator: Token, left: Node, right: Node):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOperand(Node):
    def __init__(self, operator: Token, operand: Node):
        super().__init__()
        self.operator = operator
        self.operand = operand


class CreateVariableNode(Node):
    def __init__(self, var):
        super().__init__()
        self.var = var


class NumNode(Node):
    def __init__(self, num):
        super().__init__()
        self.num = num


class BooleanNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class NodeWBody(UnaryOperand):
    def __init__(self, operator, operand, body):
        super().__init__(operator, operand)
        self.body = body


class StringNode(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class ObjNode(Node):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj


class FunctionNode(ObjNode):
    def __init__(self, func_name, params):
        super().__init__(func_name)
        self.params = params
