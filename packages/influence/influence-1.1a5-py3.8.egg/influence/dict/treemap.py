from idict import InsertableDict as IDict
class TreeMap(dict):
	def __init__(self):
		self.__tree = IDict()
	def add(self, key, value):
		if len(self.__tree) == 0:
			self.__tree.append(key, value)
		else:
			index = 0
			for k in self.__tree.keys():
				if k > key:
					break
				index += 1
			self.__tree.insert(index, key, value)
	def __contains__(self, obj):
		return obj in self.__tree.keys() or obj in self.__tree.values()
	def keys(self):
		return self.__tree.keys()
	def values(self):
		return self.__tree.values()
	def __str__(self):
		return str(self.__tree)
	def remove(self, key):
		self.__tree.remove(key)
	def pop(self):
		self.__tree.pop()
	def __len__(self):
		return len(self.__tree)
	def __iter__(self):
		self.curr = -1
		self.currkey = None
		return iter(self.__tree)
	def __next__(self):
		self.curr += 1
		if self.curr >= len(self.__dict.keys()):
			raise StopIteration
		self.currkey = list(self.__dict.keys())[self.curr]
		return f'{self.currkey}: {self.__dict[self.currkey]}'
