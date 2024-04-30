from Parser.Le import Lang
from Parser.interpreter import Interpreter

a = input()

with open(a, 'r', encoding='utf-8') as f:
    text = f.readlines()

lang = Lang("".join(text))
tokens = lang.lex_analytic()
itr = Interpreter(tokens)
a = itr.parse()
itr.run(a)

