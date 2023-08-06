class Stack(list):
	def __init__(self):
		self.__stack = []
	def push(self, obj):
		self.__stack.append(push)
	def pop(self):
		if len(self.__stack) == 0:
			raise EmptyStackError
		obj = self.__stack.pop()
		return obj
	def peek(self):
		if len(self.__stack) == 0:
			return None
		return self.__stack[len(self.__stack)-1]
	def empty(self):
		return len(self.__stack) == 0
	def __contains__(self, obj):
		for i in self.__stack:
			if i == obj:
				return True
		return False
	def index(self, element):
		for i in range(len(self.__stack)):
			if self.__stack[i] == element:
				return i
		return -1
	def __len__(self):
		return len(self.__stack)
	def __str__(self):
		string = '['
		curr = len(self.__stack) - 1
		while curr >= 0:
			if curr == 0:
				string += f'\n\t{curr}'
				continue
			string += f'\n\t{curr},'
			curr -= 1
		string += '\n]'
		return string
	def __iter__(self):
		self.curr = -1
		return iter(reversed(self.__stack))
	def __next__(self):
		self.curr += 1
		if self.curr >= len(self.__stack):
			raise StopIteration
		return reversed(self.__stack)[self.curr]

class EmptyStackError(Exception):
	def __str__(self):
		return 'pop() called on an empty stack'