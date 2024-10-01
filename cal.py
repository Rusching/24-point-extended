from typing import List, Optional
import itertools
import pdb

FINAL_GOAL = 24

class Calculator():
    def __init__(self) -> None:
        self.unary = {'', '!', '~'}
        self.bin = {'+', '-', '*', '/', '//', '>>', '<<', '|', '&', '^', '**'}
        self.factorialTable = {
            0: 1,
            1: 1,
            2: 2,
            3: 6,
            4: 24,
            5: 120,
            6: 720
        }
        self.res = []

    def unary_derive(self, op, opstr):
        isDigit = False
        if opstr.isdigit(): isDigit = True 
        res = [(op, opstr)]
        res.append((~op, "~{}".format(opstr) if isDigit else "~({})".format(opstr)))
        if 0 <= op < 7: res.append((~op, "{}!".format(opstr) if isDigit else "({})!".format(opstr)))
        return res
    
    def bin_derive(self, op1, op1str, op2, op2str):
        res = []
        for operator in self.bin:
            if operator == '/' and op2 == 0: continue
            if operator == '//' and op2 == 0: continue
            if operator == '>>' and (op2 < 0 or op2 > 10): continue
            if operator == '<<' and (op2 < 0 or op2 > 10): continue
            if operator == '**' and op1 == 0 and op2 < 0: continue
            if operator == '**' and op2 > 5: continue
            val = self.bin_perform(op1, op1str, op2, op2str, operator)
            if val == int(val):
                val = int(val)
            else: continue
            s = "({} {} {})".format(op1str, operator, op2str)
            res.append((val, s))
        return res

    def bin_perform(self, op1, op1str, op2, op2str, operator):
        try:
            if operator == '+': return op1 + op2
            elif operator == '-': return op1 - op2
            elif operator == '*': return op1 * op2
            elif operator == '/': return op1 / op2
            elif operator == '//': return op1 // op2
            elif operator == '>>': return op1 >> op2
            elif operator == '<<': return op1 << op2
            elif operator == '|': return op1 | op2
            elif operator == '&': return op1 & op2
            elif operator == '^': return op1 ^ op2
            elif operator == '**': return op1 ** op2
        except:
            print(op1, op1str, op2, op2str, operator)
            pdb.set_trace()

    def bk(self, stk):
        if len(stk) == 1:
            return self.unary_derive(stk[0], str(stk[0]))
        elif len(stk) == 2:
            op1, op2 = stk[0], stk[1]
            res = []
            for op1d, op1strd in self.unary_derive(op1, str(op1)):
                for op2d, op2strd in self.unary_derive(op2, str(op2)):
                   res.extend(self.bin_derive(op1d, op1strd, op2d, op2strd)) 
            return res
        else:
            for i in range(1, len(stk)):
                op1_packed = self.bk(stk[:i])
                op2_packed = self.bk(stk[i:])
                res = []
                for op1, op1str in op1_packed:
                    for op2, op2str in op2_packed:
                        for op1d, op1strd in self.unary_derive(op1, op1str):
                            for op2d, op2strd in self.unary_derive(op2, op2str):
                                res.extend(self.bin_derive(op1d, op1strd, op2d, op2strd))
            if len(stk) == 4:
                for v, s in res:
                    if v == FINAL_GOAL: 
                        print(s)
                        exit()
                        self.res.append(s)
            return res

    def eval(self, nums:List[int]) -> Optional[List[str]]:
        all_permus = itertools.permutations(nums)
        for each_permu in all_permus:
            self.bk(each_permu)
        
    def format(self):
        for s in self.res:
            print(s)

if __name__ == "__main__":
    cal = Calculator()
    input_numbers = input("Please input 4 numbers: (separated by space and range from 1 - 13):")
    numbers = list(map(int, input_numbers.strip().split()))
    if len(numbers) != 4 or not all(1 <= n <= 13 for n in numbers):
        print("Please input 4 numbers: (separated by space and range from 1 - 13)")
    cal.eval(numbers)
    cal.format()