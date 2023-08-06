class StringBuffer(str):
	def __init__(self, str=''): self.str = str
	def __len__(self): return len(self.str)
	def __contains__(self, obj): return str(obj) in self.str
	def __iter__(self):
		self.curr = 0
		return iter(self.str)
	def __next__(self):
		self.curr += 1
		if self.curr == len(self.str):
			raise StopIteration
		return self.str[self.curr]
	def __str__(self): return str(self.str)
	def __getitem__(self, key):
		if isinstance(key, slice):
			start, stop, step = key.indices(len(self))
			return StringBuffer(''.join([self[i] for i in range(start, stop, step)]))
		else:
			if key > len(self.str):
				raise IndexError
			return self.str[key]
	def __setitem__(self, key, item):
		if key > len(self.str):
			raise IndexError
		self.str[key] = item
	def append(self, append): self.str += append
	def index(self, obj): self.str.index(obj)
	def insert(self, index, obj): self.str = self.str[:index] + obj + self.str[index:]
	def __add__(one, two): return StringBuffer(str(one) + str(two))
	def __iadd__(self, two): self.str = str(self.str) + str(two.str)
	def replace(self, start, stop, replace): self.str = self.str[:start] + replace + self.str[stop:]
	def __delitem__(self, key): 
		if isinstance(key, slice):
			string = ''
			start, stop, step = key.indices(len(self))
			if step == None:
				step = 1
			while start < stop:
				string += self.str[start]
				start += step
			self.str = string
			return
		self.str = self.str[:key] + self.str[key+1:]