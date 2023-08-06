from influence.dict import IDict
class StemLeaf(dict):
	def __init__(self):
		self.__dict = IDict()
	def plot(self, stem, leaf):
		if stem not in self.__dict.keys():
			self.__dict[stem] = [leaf]
		else:
			l = self.__dict[stem]
			l.append(leaf)
			l.sort()
			self.__dict[stem] = l
	def remove(self, stem, leaf):
		if stem not in self.__dict:
			raise NoStemError
		elif leaf not in self.__dict[stem]:
			raise NoLeafError
		else:
			self.__dict[stem].remove(leaf)
	def __str__(self):
		string = ''
		for key in self.__dict.keys():
			string += f'{key}: '
			for i in self.__dict[key]:
				string += f'{i} '
			string += '\n'
		return string
	def empty(self):
		return len(self.__dict) == 0

class NoStemError(Exception):
	def __str__(self):
		return 'stem could not be found in plot'

class NoLeafError(Exception):
	def __str__(self):
		return 'leaf not found in stem'