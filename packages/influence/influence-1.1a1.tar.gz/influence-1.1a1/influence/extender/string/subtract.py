class Subtract:
	def subtract(initial, remove):
		if not(remove in initial):
			return initial
		index = initial.index(remove)
		tracker = 0
		removed = ''
		while tracker < len(initial):
			if not(tracker >= index and tracker < index + len(remove)):
				removed += initial[tracker:tracker + 1]
			tracker += 1
		return removed
	def subtract_all(initial, remove):
		if not(remove in initial):
			return initial
		removed = ''
		tracker = 0
		index = initial.index(remove)
		while tracker < len(initial):
			if not(tracker >= index and tracker < index + len(remove)):
				removed += initial[tracker:tracker + 1]
			if tracker == index + len(remove) - 1 and remove in initial[index + len(remove)]:
				index = initial.index(remove, index + len(remove))
			tracker += 1
		return removed

#print(Subtract.subtract("hello", "hel"))
