class Fraction:
        def __init__(self, num, denom):
                self.num = num
                self.denom = denom
        def simplify(self):
                current_value = 1
                while (current_value <= self.denom):
                        if self.num % current_value == 0 and self.denom % current_value == 0:
                                self.num = self.num / current_value
                                self.denom = self.denom / current_value
                        current_value += 1
        def __float__(self):
                return float(self.num) / float(self.denom)
        def __int__(self):
                return int(self.num / self.denom)
        def __str__(self):
                return f'{self.num}/{self.denom}'
        def equals(self, other):
                if (self.num == other.num and self.denom == other.denom) or (self.float() == other.float()):
                        return True
                return False
        def compare_to(self, other):
                return self.int() - other.int()
        def __lt__(self, other):
                if self.__float__() < other.__float__():
                        return True
                return False
        def __lte__(self, other):
                if self.__float__() <= other.__float__():
                        return True
                return False
        def __eq__(self, other):
                if self.__float__() == other.__float__():
                        return True
                return False
        def __gt__(self, other):
                if self.__float__() > other.__float__():
                        return True
                return False
        def __gte__(self, other):
                if self.__float__() >= other.__float__():
                        return True
                return False
        def __add__(a, b):
                com_denom = a.denom * b.denom
                a_num = a.num * b.denom
                b_num = b.num * a.denom
                return Fraction(a_num + b_num, com_denom)
        def __sub__(a, b):
                com_denom = a.denom * b.denom
                a_num = a.num * b.denom
                b_num = b.num * a.denom
                return Fraction(a_num - b_num, com_denom)
        def __mul__(a, b):
                return Fraction(a.num * b.num, a.denom * b.denom)
        def __truediv__(a, b):
                return Fraction(a.num * b.denom, a.denom * b.num)
        def __iadd__(a, b):
                return Fraction.__add__(a, b)
        def __isub__(a, b):
                return Fraction.__sub__(a, b)
        def __imul__(a, b):
                return Fraction.__mul__(a, b)
        def __itruediv__(a, b):
                return Fraction.__truediv__(a, b)
