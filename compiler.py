# compiler.py
class BytecodeCompiler:
    @staticmethod
    def compile_stack(ir_instructions):
        bytecode = []
        for instr in ir_instructions:
            if instr.op == 'LOAD_CONST':
                bytecode.append(('PUSH_C', instr.arg1))
            elif instr.op == 'LOAD_VAR':
                bytecode.append(('LOAD', instr.arg1))
            elif instr.op in ('ADD', 'MUL'):
                bytecode.append((instr.op,))
            elif instr.op == 'STORE_VAR':
                bytecode.append(('STORE', instr.dest))
        return bytecode

    @staticmethod
    def compile_register(ir_instructions):
        bytecode = []
        reg_map = {}
        r_counter = [0]

        def get_reg(name):
            if name not in reg_map:
                reg_map[name] = f"r{r_counter[0]}"
                r_counter[0] += 1
            return reg_map[name]

        for instr in ir_instructions:
            if instr.op == 'LOAD_CONST':
                dest_r = get_reg(instr.dest)
                bytecode.append(('MOV_CONST', dest_r, instr.arg1))
            elif instr.op == 'LOAD_VAR':
                dest_r = get_reg(instr.dest)
                bytecode.append(('MOV_VAR', dest_r, instr.arg1))
            elif instr.op in ('ADD', 'MUL'):
                dest_r = get_reg(instr.dest)
                r1 = get_reg(instr.arg1)
                r2 = get_reg(instr.arg2)
                bytecode.append((instr.op, dest_r, r1, r2))
            elif instr.op == 'STORE_VAR':
                src_r = get_reg(instr.arg1)
                bytecode.append(('STORE_VAR_REG', instr.dest, src_r))
        return bytecode