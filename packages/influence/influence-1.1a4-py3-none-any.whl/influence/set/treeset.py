class TreeSet(set):
	def __init__(self, t):
		self.t = t
		self.__set = set()
		self.__sorted = []
	def add(self, item):
		if item in self.__set:
			return False
		if not isinstance(item, t):
			raise ValueError
		self.__sorted.append(item)
		self.__sorted.sort()
		self.__set = set(self.__sorted)
		return True
	def __contains__(self, obj):
		return obj in self.__set
	def remove(self, item):
		self.__set.remove(item)
		self.__sorted.remove(item)
	def discard(self, item):
		self.__set.discard(item)
		self.__sorted.remove(item)
	def __len__(self):
		return len(self.__set)
	def __str__(self):
		return str(self.__set)
	def __iter__(self):
		self.curr = -1
		return iter(self.__set)
	def __next__(self):
		self.curr += 1
		if self.curr >= len(self.__set):
			raise StopIteration
		return self.__sorted[self.curr]
	def pop(self):
		self.__set.pop()
		self.__sorted.pop()