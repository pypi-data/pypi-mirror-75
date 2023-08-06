from stats import Stats
class Combinatorics(Stats):
	def factorial(num):
		if num == 1:
			return 1
		return num * Combinatorics.factorial(num - 1)
	def P(n, r):
		return float(Combinatorics.factorial(n)) / float(Combinatorics.factorial(n - r))
	def C(n, r):
		return float(Combinatorics.factorial(n)) / (float(Combinatorics.factorial(n-r)) * float(Combinatorics.factorial(r)))
