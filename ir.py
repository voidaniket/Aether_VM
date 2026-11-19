# ir.py
from parser import NumNode, VarNode, BinOpNode

class IRInstruction:
    def __init__(self, op, dest, arg1=None, arg2=None):
        self.op = op       # 'LOAD', 'ADD', 'MUL', 'ASSIGN'
        self.dest = dest   # Temporary variable name (e.g., 't1')
        self.arg1 = arg1
        self.arg2 = arg2

    def __repr__(self):
        return f"{self.dest} = {self.op} {self.arg1 or ''} {self.arg2 or ''}".strip()

def lower_to_ir(ast_node):
    """Lowers AST into 3-address code IR operations."""
    temp_counter = [0]
    def new_temp():
        temp_counter[0] += 1
        return f"t{temp_counter[0]}"

    ir_instructions = []

    def walk(node):
        if isinstance(node, NumNode):
            t = new_temp()
            ir_instructions.append(IRInstruction('LOAD_CONST', t, node.value))
            return t
        elif isinstance(node, VarNode):
            t = new_temp()
            ir_instructions.append(IRInstruction('LOAD_VAR', t, node.name))
            return t
        elif isinstance(node, BinOpNode):
            left_t = walk(node.left)
            right_t = walk(node.right)
            t = new_temp()
            op = 'ADD' if node.op == '+' else 'MUL'
            ir_instructions.append(IRInstruction(op, t, left_t, right_t))
            return t

    final_t = walk(ast_node.expr)
    ir_instructions.append(IRInstruction('STORE_VAR', ast_node.name, final_t))
    return ir_instructions