from io import StringIO
import sys

class EmptyStackException(Exception):
    """Raised when the program tries to pop an empty stack."""
    pass

class InvalidRegisterException(Exception):
    """Raised when the program tries to access a register that doesn't exist."""
    pass

class InvalidInstructionException(Exception):
    """Raised when the program encounters an invalid emoji."""
    pass

class MemoryOutOfBoundsException(Exception):
    """Raised when a program tries to access memory outside of its size."""
    pass

class EmoProgram:
    
    def __init__(self, F, input_values=None):
        self.P = list(F)  # Assuming F is a sequence of instructions
        self.PC = 0  # Program Counter
        self.STACK = []  # Stack
        self.R = [0] * 15  # Registers
        self.MEM = [0] * 256  # Memory
        self.ACC = None  # Accumulator
        self.input_values = iter(input_values) if input_values else iter([])
        self.NUMS = {ch: i for i, ch in enumerate('0123456789⓿⓵⓶⓷⓸⓹⓺⓻⓼⓽')}
        self.EMO = {
            '🌞': self.emo_func_start,
            '📥': self.emo_func_input_byte,
            '🔼': self.emo_func_push_byte,
            '⊕': self.emo_func_xor_byte,
            '❔': self.emo_func_if,
            '🚫': self.emo_func_if_not,
            '🟰': self.emo_func_compare,
            '≪': self.emo_func_shift_left,
            '≫': self.emo_func_shift_right,
            '🎎': self.emo_func_and,
            '🏮': self.emo_func_or,
            '🔄': self.emo_func_swap_mem,
            '🔁': self.emo_func_jump_back,
            '': self.emo_func_jump_forward,
            '📈': self.emo_func_mov_to_register,
            '📰': self.emo_func_copy_to_register,
            '📉': self.emo_func_mov_from_register,
            '📎': self.emo_func_push_pc,
            '📌': self.emo_func_pop_to_pc,
            '🚀': self.emo_func_absolute_jump,
            '📝': self.emo_func_write_memory,
            '📕': self.emo_func_read_memory,
            '➖': self.emo_func_subtract,
            '➕': self.emo_func_add,
            '➗': self.emo_func_mod,
            '🔊': self.emo_func_output_byte,
            '📞': self.emo_func_call,
            '🪄': self.emo_func_return,
            '📝': self.emo_func_nop
        }
        self.output = StringIO()
        self.emoji_digits = {
            '⓿': 0, '⓵': 1, '⓶': 2, '⓷': 3, '⓸': 4,
            '⓹': 5, '⓺': 6, '⓻': 7, '⓼': 8, '⓽': 9
        }

    def get_next_value(self):
        value = ""
        while self.PC + 1 < len(self.P) and self.P[self.PC + 1] in self.emoji_digits:
            self.PC += 1
            value += str(self.emoji_digits[self.P[self.PC]])
        return int(value) if value else 0
    
    def emo_func_start(self, I=None):
        pass
    
    def emo_func_input_byte(self, I=None):
        try:
            V = next(self.input_values)  # Get the next input value
            print(f"INPUT {V}")
            self.STACK.append(V)
        except StopIteration:
            raise InvalidInstructionException("No more input values available")
    
    def emo_func_push_byte(self, I=None):
        byte_value = self.get_next_value()
        print(f"PUSH {byte_value}")
        self.STACK.append(byte_value)
    
    def emo_func_push_pc(self, I=None):
        self.STACK.append(self.PC)
        print(f"PUSH_PC: Pushed PC {self.PC} onto stack")
    
    def emo_func_swap_mem(self, I=None):
        value1 = self.get_next_value()
        digits = [int(digit) for digit in str(value1)]
        if len(digits) < 3:
            digits = [0] * (3 - len(digits)) + digits
        else:
            digits = digits[-3:]
        array = [self.NUMS[str(digit)] for digit in digits]
        R1 = self.NUMS[str(array[1])]
        R2 = self.NUMS[str(array[2])] 
        temp = self.MEM[R1]
        self.MEM[R1] = self.MEM[R2]
        self.MEM[R2] = temp
        print(f"SWAP_MEM: Swapped MEM[{R1}] and MEM[{R2}]")
    
    def emo_func_absolute_jump(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        self.PC = self.R[R1]
        print(f"ABSOLUTE_JUMP: Jumped to {self.PC}")
    
    def emo_func_pop_to_pc(self, I=None):
        if not self.STACK:
            raise EmptyStackException()
        self.PC = self.STACK.pop()
        print(f"POP_TO_PC: Popped {self.PC} to PC")
    
    def emo_func_call(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        self.STACK.append(self.PC)
        self.PC = self.R[R1]
        print(f"CALL: Called {self.PC}")
    
    def emo_func_nop(self, I=None):
        pass
        print(f"NOP: No operation")
    
    def emo_func_return(self, I=None):
        if not self.STACK:
            raise EmptyStackException()
        self.PC = self.STACK.pop()
        print(f"RETURN: Returned to {self.PC}")
    
    def emo_func_xor_byte(self, I=None):
        value1 = self.get_next_value()
        print(value1)
        if len(self.STACK) > 1:
            V1 = self.STACK.pop()
            print(V1)
            V2 = self.STACK.pop()
            result = V1 ^ V2
            print(f"XOR {V1} ^ {V2} = {result}")
            self.STACK.append(result)
        else:
            raise EmptyStackException()
    
    def emo_func_and(self, I=None):
        value1 = self.get_next_value()
        digits = [int(digit) for digit in str(value1)]
        if len(digits) < 3:
            digits = [0] * (3 - len(digits)) + digits
        else:
            digits = digits[-3:]
        array = [self.NUMS[str(digit)] for digit in digits]
        print(array)
        intial = self.MEM[2]
        print(intial)
        R1 = self.NUMS[str(array[0])] 
        R2 = self.NUMS[str(array[1])] 
        R3 = self.NUMS[str(array[2])] 
        self.R[R3] = self.R[R1] & self.R[R2]
        print(f"AND: {R3} = {R1} & {R2} = {self.R[R3]}")
    
    def emo_func_or(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        R3 = self.NUMS[I[3]] - 1
        self.R[R3] = self.R[R1] | self.R[R2]
        print(f"OR: R{R3} = R{R1} | R{R2} = {self.R[R3]}")
    
    def emo_func_shift_left(self, I=None):
        value1 = self.get_next_value()
        digits = [int(digit) for digit in str(value1)]
        if len(digits) < 4:
            digits = [0] * (4 - len(digits)) + digits
        else:
            digits = digits[-4:]
        array = [self.NUMS[str(digit)] for digit in digits]
        print(array)
        R1 = self.NUMS[str(array[0])]
        R2 = self.NUMS[str(array[2])]
        self.R[R1] <<= self.R[R2]
        print(f"SHIFT LEFT: R{R1} <<= {R2}")
    
    def emo_func_shift_right(self, I=None):
        value1 = self.get_next_value()
        digits = [int(digit) for digit in str(value1)]
        if len(digits) < 4:
            digits = [0] * (4 - len(digits)) + digits
        else:
            digits = digits[-4:]
        array = [self.NUMS[str(digit)] for digit in digits]
        print(array)
        R1 = self.NUMS[str(array[0])]
        R2 = self.NUMS[str(array[3])]
        self.R[R1] >>= self.R[R2]
        print(f"SHIFT_RIGHT: R{R1} >>= {R2}")
        print(self.NUMS[R1])
    
    def emo_func_compare(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        self.ACC = self.R[R1] == self.R[R2]
        print(f"COMPARE: ACC = R{R1} == R{R2} -> {self.ACC}")
    
    def emo_func_if(self, I=None):
        if self.ACC:
            self.PC = self.NUMS[I[1]] - 1
        print(f"IF: PC = {self.PC} if ACC == {self.ACC}")
    
    def emo_func_if_not(self, I=None):
        if not self.ACC:
            self.PC = self.NUMS[I[1]] - 1
        print(f"IF_NOT: PC = {self.PC} if ACC == {self.ACC}")
    
    def emo_func_jump_back(self, I=None):
        self.PC -= self.NUMS[I[1]]
        print(f"JUMP_BACK: PC = {self.PC}")

    def emo_func_jump_forward(self, I=None):
        self.PC += self.NUMS[I[1]]
        print(f"JUMP_FORWARD: PC = {self.PC}")

    def emo_func_mov_to_register(self, I=None):
        if len(self.STACK) > 0:    
            R1 = self.STACK.pop()
            R2 = self.get_next_value()
            self.R[R2] = R1
            print(f"{R1} MOVED TO {R2}")
            return None
        raise None


    def emo_func_copy_to_register(self, I=None):
        if not self.STACK:
            raise EmptyStackException()
        R1 = self.NUMS[I[1]] - 1
        self.R[R1] = self.STACK[-1]
        print(f"COPIED TO REGISTER: PC = {self.PC}")

    def emo_func_mov_from_register(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        self.STACK.append(self.R[R1])
        print(f"MOVE FROM REGISTER: PC = {self.PC}")

    def emo_func_subtract(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        R3 = self.NUMS[I[3]] - 1
        self.R[R3] = self.R[R1] - self.R[R2]
    
    def emo_func_add(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        R3 = self.NUMS[I[3]] - 1
        self.R[R3] = self.R[R1] + self.R[R2]
    
    def emo_func_mod(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        R3 = self.NUMS[I[3]] - 1
        self.R[R3] = self.R[R1] % self.R[R2]
    
    def emo_func_write_memory(self, I=None):
        R1 = self.NUMS[I[1]] - 1
        R2 = self.NUMS[I[2]] - 1
        if self.R[R2] >= len(self.MEM):
            raise MemoryOutOfBoundsException()
        self.MEM[self.R[R2]] = self.R[R1]
    
    def emo_func_read_memory(self, I=None):
        value1 = self.get_next_value()
        digits = [int(digit) for digit in str(value1)]
        if len(digits) < 3:
            digits = [0] * (3 - len(digits)) + digits
        else:
            digits = digits[-3:]
        array = [self.NUMS[str(digit)] for digit in digits]
        R1 = self.NUMS[str(array[0])]
        R2 = self.NUMS[str(array[1])]
        if self.R[R1] >= len(self.MEM):
            raise MemoryOutOfBoundsException()
        self.R[R2] = self.MEM[R1]
        print(f"READ FROM MEMORY SET R2 TO R1 {R1},{R2}")

    def emo_func_output_byte(self, I=None):
        if len(self.STACK) > 0:
            V = self.STACK.pop()
            print(f"OUTPUT: {chr(V)}")
            self.output.write(chr(V))
    
    def run_program(self):
        while self.PC < len(self.P):
            I = self.P[self.PC]
            print(f"PC: {self.PC}, Instruction: {I}, Stack: {self.STACK}")
            if I in self.emoji_digits:
                self.PC += 1
                continue
            fn = self.EMO.get(I)
            if fn:
                fn(I)
            else:
                raise InvalidInstructionException(f"Invalid instruction: {I}")
            self.PC += 1

        return self.output.getvalue()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ./runtime.py input_file.emo')
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        file_content = f.read()
    input_values = [83,73,86,85,83,67,71,123,101,109,48,116,49,111,110,52,108,95,100,52,109,52,103,51,125]  # Example input values
    program = EmoProgram(file_content, input_values)
    output = program.run_program()
    print(output)
