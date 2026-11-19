# vm.py
class VirtualMachine:
    def __init__(self):
        self.variables = {}

    def run_stack(self, bytecode):
        stack = []
        for instr in bytecode:
            op = instr[0]
            if op == 'PUSH_C':
                stack.append(instr[1])
            elif op == 'LOAD':
                stack.append(self.variables.get(instr[1], 0))
            elif op == 'ADD':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif op == 'MUL':
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            elif op == 'STORE':
                self.variables[instr[1]] = stack.pop()

    def run_register(self, bytecode):
        regs = {}
        for instr in bytecode:
            op = instr[0]
            if op == 'MOV_CONST':
                regs[instr[1]] = instr[2]
            elif op == 'MOV_VAR':
                regs[instr[1]] = self.variables.get(instr[2], 0)
            elif op == 'ADD':
                regs[instr[1]] = regs[instr[2]] + regs[instr[3]]
            elif op == 'MUL':
                regs[instr[1]] = regs[instr[2]] * regs[instr[3]]
            elif op == 'STORE_VAR_REG':
                self.variables[instr[1]] = regs[instr[2]]


class AetherAdaptiveRuntime:
    """Implements AETHER's cost-minimization selection policy[cite: 6]."""
    def __init__(self):
        self.vm = VirtualMachine()
        self.function_stats = {}

    def estimate_cost(self, mode, bytecode_size, invocation_count):
        """
        AETHER Cost Model approximation based on Section 5.1:
        J(f, r) = alpha * Time + gamma * Footprint + delta * Profiling[cite: 6]
        """
        if mode == 'stack':
            # Stack execution takes more instructions (higher time proxy), but smaller bytecode footprint
            time_cost = invocation_count * 1.5
            footprint_cost = bytecode_size * 1.0
        else:
            # Register execution takes fewer instructions (lower time proxy), but larger bytecode footprint
            time_cost = invocation_count * 1.0
            footprint_cost = bytecode_size * 1.8
        
        # Weights (alpha = 1.0, gamma = 0.5)
        return (1.0 * time_cost) + (0.5 * footprint_cost)

    def execute_function(self, func_name, stack_code, reg_code):
        if func_name not in self.function_stats:
            self.function_stats[func_name] = {
                'invocations': 0, 
                'mode': 'stack',
                'stack_size': len(stack_code),
                'reg_size': len(reg_code)
            }

        stats = self.function_stats[func_name]
        stats['invocations'] += 1

        # Run AETHER's cost-minimization calculation after observation threshold[cite: 6, 7]
        if stats['invocations'] == 3:
            cost_stack = self.estimate_cost('stack', stats['stack_size'], stats['invocations'])
            cost_reg = self.estimate_cost('register', stats['reg_size'], stats['invocations'])
            
            print(f"\n[Cost Model Evaluation for '{func_name}']> Stack Cost: {cost_stack:.1f} | Register Cost: {cost_reg:.1f}")
            
            if cost_reg < cost_stack:
                print(f"-> Policy decision: Register cost is lower. Switching representation!\n")
                stats['mode'] = 'register'
            else:
                print(f"-> Policy decision: Retaining stack representation.\n")

        # Execute using the active representation
        if stats['mode'] == 'stack':
            print(f"[{func_name}] Executing Stack Bytecode (Call #{stats['invocations']})")
            self.vm.run_stack(stack_code)
        else:
            print(f"[{func_name}] Executing Register Bytecode (Call #{stats['invocations']})")
            self.vm.run_register(reg_code)