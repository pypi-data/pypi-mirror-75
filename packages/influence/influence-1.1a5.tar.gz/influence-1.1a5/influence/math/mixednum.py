from frac import Fraction
class MixedNumber:
        def __init__(self, coeff, num, denom):
                self.coeff = coeff
                self.num = num
                self.denom = denom
                self.fraction = Fraction(num, denom)
        def simplify(self):
                current_value = 1
                while (current_value <= self.denom):
                        if self.num % current_value == 0 and self.denom % current_value == 0:
                                self.num /= current_value
                                self.denom /= current_value
                        curent_value += 1
                while self.num >= self.denom:
                        self.num -= self.denom
                        self.coeff += 1
                self.fraction = Fraction(self.num, self.denom)
                self.fraction.simplify()
        def __float__(self):
                return float(self.coeff * self.denom + self.num) / float(self.denom)
        def __int__(self):
                return int((self.coeff * self.denom + self.num) / self.denom)
        def __str__(self):
                return f'{self.coeff} {self.num}/{self.denom}'
        def equals(self, other):
                if (self.coeff == other.coeff and self.num == other.num and self.denom == other.denom) or (self.float() == other.float()):
                        return True
                return False
        def compare_to(self, other):
                return self.int() - other.int()
        def to_fraction(self):
                new_num = self.coeff * self.denom + self.num
                return Fraction(new_num, self.denom)
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
                fa = a.to_fraction()
                fb = b.to_fraction()
                coeff = 0
                add = fa + fb
                copy = add.num
                while copy > add.denom:
                        copy -= add.denom
                        coeff += 1
                if coeff == 0:
                        return MixedNumber(0, copy, add.denom)
                return MixedNumber(coeff, copy, add.denom)
        def __sub__(a, b):
                fa = a.to_fraction()
                fb = b.to_fraction()
                sub = fa - fb
                copy = sub.num
                coeff = 0
                while copy > sub.denom:
                        copy -= sub.denom
                        coeff += 1
                if coeff == 0:
                        return MixedNumber(0, copy, sub.denom)
                return MixedNumber(coeff, copy, sub.denom)
        def __mul__(a, b):
                fa = a.to_fraction()
                fb = b.to_fraction()
                mul = fa * fb
                copy = mul.num
                coeff = 0
                while copy > mul.denom:
                        copy -= mul.denom
                        coeff += 1
                if coeff == 0:
                        return MixedNumber(0, copy, mul.denom)
                return MixedNumber(coeff, copy, mul.denom)
        def __truediv__(a, b):
                fa = a.to_fraction()
                fb = b.to_fraction()
                div = fa / fb
                copy = div.num
                coeff = 0
                while copy > div.denom:
                        copy -= div.denom
                        coeff += 1
                if coeff == 0:
                        return MixedNumber(0, copy, div.denom)
                return MixedNumber(coeff, copy, div.denom)
        def __iadd__(a, b):
                return MixedNumber.__add__(a, b)
        def __isub__(a, b):
                return MixedNumber.__sub__(a, b)
        def __imul__(a, b):
                return MixedNumber.__mul__(a, b)
        def __itruediv__(a, b):
                return Fraction.__truediv__(a, b)
        

