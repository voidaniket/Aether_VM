# parser.py
class ASTNode: pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class AssignNode(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, type_):
        tok = self.peek()
        if tok and tok.type == type_:
            self.pos += 1
            return tok
        raise RuntimeError(f"Expected token {type_}, got {tok}")

    def parse(self):
        # Parse multiple assignment statements
        statements = []
        while self.peek() is not None:
            ident = self.consume('IDENT')
            self.consume('ASSIGN')
            expr = self.expr()
            statements.append(AssignNode(ident.value, expr))
        return ProgramNode(statements)

    def expr(self):
        node = self.term()
        while self.peek() and self.peek().type == 'PLUS':
            op = self.consume('PLUS').value
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek() and self.peek().type == 'MUL':
            op = self.consume('MUL').value
            node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.consume('NUMBER')
            return NumNode(tok.value)
        elif tok.type == 'IDENT':
            self.consume('IDENT')
            return VarNode(tok.value)
        elif tok.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.expr()
            self.consume('RPAREN')
            return node
        raise RuntimeError(f"Unexpected token in factor: {tok}")