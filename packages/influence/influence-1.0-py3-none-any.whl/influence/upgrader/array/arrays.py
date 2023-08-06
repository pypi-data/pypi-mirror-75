#import unittest
import warnings

class Array:

    def __init__(self, capacity):
        self.capacity = capacity
        self.__arr = Array.__create_arr(self.capacity)

    def __create_arr(capacity):
        l = []
        for i in range(capacity):
            l.append(None)
        return l

    def get(self, index):
        warnings.warn("get is deprecated, square bracket notation preferred", DeprecationWarning)
        if index > self.capacity - 1:
            raise IndexError
        return self.__arr[index]

    def __getitem__(self, key):
        if key > self.capacity - 1:
            raise IndexError
        return self.__arr[key]

    def set(self, index, item):
        warnings.warn("set is deprecated, square bracket notation preferred", DeprecationWarning)
        if index > self.capacity - 1:
            raise IndexError
        self.__arr[index] = item

    def __setitem__(self, key, item):
        if key > self.capacity - 1:
            raise IndexError
        self.__arr[key] = item

    def __iter__(self):
        self.__itervalue = -1
        return iter(self.__arr)

    def print(self):
        if self.capacity == 0:
            print('()')
            return
        printable = f'({self.get(0)}'
        for item in self.__arr:
            printable += ', ' + item
        printable += ')'
        print(printable)

    def contains(self, item):
        for i in self.__arr:
            if i == item:
                return True
        return False

    def __contains__(self, item):
        for i in self.__arr:
            if i == item:
                return True
        return False

    def index(self, item):
        index = 0
        for i in self.__arr:
            if i == item:
                return index
            index += 1
        return -1

    def __len__(self):
        return len(self.__arr)

    def __not__(obj):
        if obj.capacity == 0:
            return False
        return True

    def __next__(self):
        self.__itervalue += 1
        if self.__itervalue == len(self.__arr):
            raise StopIteration
        return self.__arr[self.__itervalue]
'''
class TestArr(unittest.TestCase):

    def test_get_and_set(self):
        a = Array(5)
        a.set(2, "hello")
        self.assertEqual(a.get(2), "hello")

    def test_iter(self):
        pass

    def test_print(self):
        pass

    def test_contains1(self):
        a = Array(5)
        a.set(1, "hello")
        self.assertEqual(a.contains("hello"), True)
        self.assertEqual(a.contains("nohello"), False)

    def test_contains2(self):
        a = Array(5)
        a.set(1, "hello")
        self.assertEqual("hello" in a, True)
        self.assertEqual("nohello" in a, False)

    def test_find(self):
        a = Array(5)
        a.set(0, "hello")
        self.assertEqual(a.find("hello"), 0)
        self.assertEqual(a.find("nohello"), -1)

if __name__ == '__main__':
    unittest.main()
'''
