class Stats:
	def min(dataset):
		value = dataset[0]
		for data in dataset:
			if data < value:
				value = data
		return value
	def max(dataset):
		value = dataset[0]
		for data in dataset:
			if data > value:
				value = data
		return value
	def range(dataset):
		return Stats.max(dataset) - Stats.min(dataset)
	def mean(dataset):
		total = 0
		terms = 0
		for value in dataset:
			total += value
			terms += 1
		return float(total) / float(terms)
	def variance(dataset):
		terms = 0
		total = 0.0
		for value in dataset:
			total += (value - Stats.mean(dataset))**(2)
			terms += 1
		return float(total) / float(terms)
	def standard_deviation(dataset):
		return Stats.variance(dataset)**(1.0/2.0)
	def median(dataset):
		dataset.sort()
		if len(dataset) % 2 == 0:
			value_1 = dataset[int(len(dataset) / 2)]
			value_2 = dataset[int(len(dataset) / 2 - 1)]
			return (float(value_1) + float(value_2)) / 2
		else:
			return dataset[int(len(dataset) / 2)]
	def mode(dataset):
		dataset.sort()
		occurences = {}
		tracker = 0
		while tracker < len(dataset):
			if f'{dataset[tracker]}' not in occurences.keys():
				occurences[f'{dataset[tracker]}'] = 1
			else:
				occurences[f'{dataset[tracker]}'] += 1
			tracker += 1
		greatest = -100000000000
		for key in occurences.keys():
			if occurences[key] > greatest:
				greatest = occurences[key]
		greatest_list = []
		for key in occurences.keys():
			if occurences[key] == greatest:
				greatest_list.append(key)
		return greatest_list
