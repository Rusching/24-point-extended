from typing import List, Optional
import itertools
from collections import deque
import pdb

FINAL_GOAL = 24

class Calculator():
    def __init__(self) -> None:
        self.unary = {'', '!', '~'}
        self.bin = {'+', '-', '*', '/', '//', '>>', '<<', '|', '&', '^', '**'}
        self.res = []

    def bin_derive(self, op1, op1str, op2, op2str):
        res = []
        for operand in self.bin:
            if operand == '/' and op2 == 0: continue
            if operand == '//' and op2 == 0: continue
            if operand == '>>' and (op2 < 0 or op2 > 10): continue
            if operand == '<<' and (op2 < 0 or op2 > 10): continue
            if operand == '**' and op1 == 0 and op2 < 0: continue
            if operand == '**' and op2 > 5: continue
            val = self.bin_perform(op1, op1str, op2, op2str, operand)
            if val == int(val):
                val = int(val)
            else: continue
            s = "({} {} {})".format(op1str, operand, op2str)
            res.append((val, s))
        return res

    def bin_perform(self, op1, op1str, op2, op2str, operand):
        try:
            if operand == '+': return op1 + op2
            elif operand == '-': return op1 - op2
            elif operand == '*': return op1 * op2
            elif operand == '/': return op1 / op2
            elif operand == '//': return op1 // op2
            elif operand == '>>': return op1 >> op2
            elif operand == '<<': return op1 << op2
            elif operand == '|': return op1 | op2
            elif operand == '&': return op1 & op2
            elif operand == '^': return op1 ^ op2
            elif operand == '**': return op1 ** op2 
        except:
            print(op1, op1str, op2, op2str, operand)
            pdb.set_trace()

    def bk(self, stk):
        if len(stk) == 1:
            return [(stk[0], str(stk[0]))]
        elif len(stk) == 2:
            op1, op2 = stk[0], stk[1]
            return self.bin_derive(op1, str(op1), op2, str(op2))
        else:
            for i in range(1, len(stk)):
                op1_packed = self.bk(stk[:i])
                op2_packed = self.bk(stk[i:])
                res = []
                for op1, op1str in op1_packed:
                    for op2, op2str in op2_packed:
                        res.extend(self.bin_derive(op1, op1str, op2, op2str))
            if len(stk) == 4:
                for v, s in res:
                    if v == FINAL_GOAL: 
                        print(s)
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
    cal.eval([3, 3, 8, 8])
    cal.format()