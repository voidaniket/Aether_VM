# main.py
from lexer import lex
from parser import Parser
from ir import lower_to_ir
from compiler import BytecodeCompiler
from vm import AetherAdaptiveRuntime

def main():
    # Multi-line source code example
    source_code = """
    x = 10 + 5
    y = x * 2
    result = y + 4
    """
    print(f"Source Program:\n{source_code.strip()}\n")

    # 1. Frontend & IR Lowering
    tokens = lex(source_code)
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Flatten IR for all statements in the program node
    ir = []
    for stmt in ast.statements:
        ir.extend(lower_to_ir(stmt))

    print("--- Shared Intermediate Representation (IR) ---")
    for instr in ir:
        print(instr)
    print()

    # 2. Dual Bytecode Compilation[cite: 1]
    stack_bc = BytecodeCompiler.compile_stack(ir)
    reg_bc = BytecodeCompiler.compile_register(ir)

    # 3. Adaptive Execution Runtime[cite: 6]
    runtime = AetherAdaptiveRuntime()
    func_name = "compute_pipeline"

    for i in range(5):
        runtime.execute_function(func_name, stack_bc, reg_bc)
        print(f"Current Variables State: {runtime.vm.variables}\n")

if __name__ == "__main__":
    main()