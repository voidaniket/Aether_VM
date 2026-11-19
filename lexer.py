# lexer.py
import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

def lex(code):
    token_spec = [
        ('NUMBER',   r'\d+'),
        ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
        ('ASSIGN',   r'='),
        ('PLUS',     r'\+'),
        ('MUL',      r'\*'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('SKIP',     r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]
    # Fixed the f-string syntax here:
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {repr(value)}')
        tokens.append(Token(kind, value))
    return tokens