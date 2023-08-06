from multilist import List2D
class RaggedList(List2D):
        def __init__(self, rows = 1, cols = 1):
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
        def print(self):
                for row in self.__lists:
                        if len(row) == 0:
                                print('[None]')
                                continue
                        for item in row:
                                print(item, end = ' ')
                        print()
        def in_bounds(self, r_index, c_index):
                if r_index < len(self.__lists):
                        if c_index < len(self.__lists[r_index]):
                                return True
                return False
        def __extend_bounds(self, r_index, c_index):
                while r_index >= len(self.__lists):
                        temp_row = []
                        self.__lists.append(temp_row)
                while c_index >= len((self.__lists[r_index])):
                        self.__lists[r_index].append(None)
        def set(self, r_index, c_index, item):
                if RaggedList.in_bounds(self, r_index, c_index):
                        self.__lists[r_index][c_index] = item
                else:
                        RaggedList.__extend_bounds(self, r_index, c_index)
                        self.__lists[r_index][c_index] = item
        def get(self, r_index, c_index):
                if r_index < len(self.__lists):
                        if c_index < len(self.__lists[r_index]):
                                return self.__lists[r_index][c_index]
                return None
        def remove(self, r_index, c_index):
                if r_index < len(self.__lists):
                        if c_index < len(self.__lists[r_index]):
                                del self.__lists[r_index][c_index]
                                return True
                return False
        def __contains__(self, item):
                for row in self.__lists:
                        for list_item in row:
                                if item == list_item:
                                        return True
                return False
        def contains(self, item):
                for row in self.__lists:
                        for list_item in row:
                                if item == list_item:
                                        return True
                return False
        def index(self, item):
                if self.contains(item):
                        r = 0
                        c = 0
                        for row in self.__lists:
                                for list_item in row:
                                        if list_item == item:
                                                return [r, c]
                                        c += 1
                                r += 1
                                c = 0
                return [-1]
        def __len__(self):
                return len(self.__lists)
