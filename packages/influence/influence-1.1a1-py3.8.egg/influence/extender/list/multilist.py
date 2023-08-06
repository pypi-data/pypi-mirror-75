import warnings
class List2D:
        def __init__(self, rows=1, cols=1):
                self.rows = rows
                self.cols = cols
                self.__lists = []
                r = 0
                c = 0
                temp_row = []
                while r < rows:
                        while c < cols:
                                temp_row.append(None)
                                c += 1
                        self.__lists.append(temp_row)
                        c = 0
                        temp_row = []
                        r += 1
        def __getitem__(self, key):
                if key > self.rows - 1:
                        raise IndexError
                return self.__lists[key]
        def __setitem__(self, key, item):
                if key > self.cols - 1:
                        raise IndexError
                elif not isinstance(item, list):
                        raise ValueError
                self.__lists[key] = item
        def set(self, r_index, c_index, item):
                warnings.warn("set is deprecated, square bracket notation preferred", DeprecationWarning)
                if r_index < self.rows and c_index < self.cols:
                        self.__lists[r_index][c_index] = item
                        return True
                return False
        def get(self, r_index, c_index):
                warnings.warn("get is deprecated, square bracket notation preferred", DeprecationWarning)
                if r_index < self.rows and c_index < self.cols:
                        return self.__lists[r_index][c_index]
                return None
        def print(self):
                for row in self.__lists:
                        for item in row:
                                print(item, end = ' ')
                        print()
        def remove(self, r_index, c_index):
                if r_index < self.rows and c_index < self.cols:
                        self.__lists[r_index][c_index] = None
                        return True
                return False
        def contains(self, item):
                for row in self.__lists:
                        for value in row:
                                if item == value:
                                        return True
                return False
        def __contains__(self, item):
                for row in self.__lists:
                        for value in row:
                                if item == value:
                                        return True
                return False
        def index(self, item):
                if self.contains(item):
                        r = 0
                        c = 0
                        for row in self.__lists:
                                for list_item in item:
                                        if list_item == item:
                                                return [r, c]
                                        c += 1
                                r += 1
                                c = 0
                return [-1]
        def __len__(self):
                return len(self.__lists)
        def __str__(self):
                string = ''
                for i in self.__lists:
                        for j in i:
                                string += j + ' '
                        string += '\n'
                return string
        def __delitem__(self, key):
                if key > self.rows - 1:
                        raise IndexError
                del self.__lists[key]
'''
add to arrays and list
__delitem__ (list)
__str__
__getitem__ with slice
__add__
__iadd__
'''