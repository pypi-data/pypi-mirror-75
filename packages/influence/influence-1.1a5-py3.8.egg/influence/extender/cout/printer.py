class Printer:
	def print_list(this_list):
		for item in this_list:
			print(item, end = ' ')
	def print_tuple(this_tuple):
		for item in this_tuple:
			print(item, end = ' ')
	def print_dictionary(this_dictionary):
		for key in this_dictionary.keys():
			print(f'{key} : {this_dictionary[key]}')
	def print_all(ender, *items):
		if ender == False:
			for item in items:
				print(item)
		else:
			for item in items:
				print(item, end = ' ')
