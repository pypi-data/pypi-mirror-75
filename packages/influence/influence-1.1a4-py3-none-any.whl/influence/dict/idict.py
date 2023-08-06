class InsertableDict(dict):
	def __init__(self):
		self.__dict = {}
	def __getitem__(self, key):
		if key in self.__dict.keys():
			return self.__dict[key]
		raise KeyError
	def __len__(self):
		return len(self.__dict)
	def get(self, key):
		if key in self.__dict.keys():
			return self.__dict[key]
		return None
	def __setitem__(self, key, item):
		if key in self.__dict.keys():
			self.__dict[key] = item
		else:
			self.__dict[key] = item
	def append(self, key, item):
		self.__dict[key] = item
	def keys(self):
		return self.__dict.keys()
	def values(self):
		return self.__dict.values()
	def __str__(self):
		return str(self.__dict)
	def __iter__(self):
		self.curr = -1
		self.currkey = None
		return iter(self.__dict)
	def remove(self, key):
		del self.__dict[key]
	def pop(self):
		k = list(self.__dict.keys())(len(self.__dict.keys())-1)
		del self.__dict[k]
	def __next__(self):
		self.curr += 1
		if self.curr >= len(self.__dict.keys()):
			raise StopIteration
		self.currkey = list(self.__dict.keys())[self.curr]
		return f'{self.currkey}: {self.__dict[self.currkey]}'
	def insert(self, index, key, value):
		allocated = {}
		i = 0
		for k in self.__dict.keys():
			if i != index:
				allocated[k] = self.__dict[k]
				i += 1
			else:
				allocated[key] = value
				allocated[k] = self.__dict[k]
				i += 1
		self.__dict = allocated
'''