from arrays import Array
import warnings

class Array2D(Array):

    def __init__(self, r, c):
        self.capacity = r
        self.__arr = Array2D.__create_arr(r, c)

    def __create_arr(r, c):
        arr = []
        for i in range(r):
            arr.append(Array(c))
        return arr

    def __getitem__(self, key):
        if key > self.capacity - 1:
            raise IndexError
        return self.__arr[key]

    def __setitem__(self, key, item):
        if key > self.capacity - 1:
            raise IndexError
        elif not isinstance(item, Array):
            raise ValueError
        self.__arr[key] = item

    def get(self, r_index, c_index):
        warnings.warn("get is deprecated, square bracket notation preferred", DeprecationWarning)
        if r_index > self.capacity - 1 or c_index > self.__arr[0].capacity - 1:
            raise IndexError
        return (self.__arr[r_index])[c_index]

    def set(self, r_index, c_index, item):
        warnings.warn("set is deprecated, square bracket notation preferred", DeprecationWarning)
        if r_index > self.capacity - 1 or c_index > self.__arr[0].capacity - 1:
            raise IndexError
        self.__arr[r_index].__setitem__(c_index, item)

    def print(self):
        if self.capacity == 0:
            print('()')
            return
        for i in self.__arr:
            i.print()

    def contains(self, item):
        for i in self._arr:
            for j in i:
                if j == item:
                    return True
        return False

    def __contains__(self, item):
        for i in self._arr:
            for j in i:
                if j == item:
                    return True
        return False

    def index(self, item):
        r_index = 0
        c_index = 0
        for i in self.__arr:
            for j in i:
                c_index = 0
                if i == item:
                    return [r_index, c_index]
                c_index += 1
            r_index += 1
        return [-1]

    def __len__(self):
        return len(self.__arr)