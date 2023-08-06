class AsList:
	def character_list(string):
		chars = []
		tracker = 0
		while tracker < len(string):
			chars.append(string[tracker:tracker + 1])
			tracker += 1
		return chars
	def word_list(string):
		words = []
		tracker = 0
		temp_str = ''
		while tracker < len(string):
			char = string[tracker:tracker + 1]
			if char != ' ':
				temp_str += char
			else:
				words.append(temp_str)
				temp_str = ''
			tracker += 1
		words.append(temp_str)
		return words
	def word_list_with_spaces(string):
		words = []
		tracker = 0
		temp_str = ''
		while tracker < len(string):
			char = string[tracker:tracker + 1]
			if char != ' ':
				temp_str += char
			else:
				words.append(temp_str)
				words.append(' ')
				temp_str = ''
			tracker += 1
		words.append(temp_str)
		return words
