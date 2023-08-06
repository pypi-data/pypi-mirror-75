Influence - The Python Extender You Asked For
=============================================

With influence you can extend python with things like two-dimensional
lists, fractions, string subtractors, etc. You can also upgrade python
with things it doesn't have like arrays!

Overview
========

The influence python library was created with one sole purpose, helping
you do things that can't be done in standard python with ease

Usage
=====

Below is how to install and use the influence library in your own
programs!

Installation
~~~~~~~~~~~~

.. code:: sh

    $ pip install influence
    or 
    $ python3 -m pip install -U influence

The influence package has two package dependencies, numpy and matplotlib
(used for grapher and agrapher classes)

Cout
''''

Cout (common output) has only one class, printer, that helps print
tuples, lists, dicts, etc. nicely

Importing:

.. code:: py

    from influence import cout
    #or
    from influence.cout import Printer

Printer Class
             

Methods:

.. code:: py

    Printer.print_list(list) #prints a list nicely
    Printer.print_tuple(tuple) #prints a tuple nicely
    Printer.print_dictionary(dict) #prints a dict nicely
    Printer.print_all(ender, *items) 
    #prints all of items, if ender is False, prints each item on new line
    #else all items are printed on the same line

Cin
'''

Cin (common input), has one class, input, that handles input
specifically

Importing:

.. code:: py

    from influence import cin
    #or 
    from influence.cin import Input

Input Class
           

Methods:

.. code:: py

    value = Input.input(t, prompt=None)
    #stores input into value
    #prompt will be printed, defaults to None
    #raises ValueError if input does not match type t
    #raises TypeError if t not able to be casted from input

List2D Class
            

Creates a 2D list of a square size

Importing:

.. code:: py

    from influence.list import multilist
    #or
    from influence.list.multilist import List2D

Initializing:

.. code:: py

    l = List2D(rows=1, cols=1) 
    #creates the list to have rows number of rows and cols number of cols

Methods:

.. code:: py

    l[r_index][c_index] = item
    #sets value at r_index and c_index to item
    #raises IndexError if index out of bounds
    l[r_index].append(item)
    #since this is a list, if you wish to append the list
    #you can do it this way instead of settings
    l[r_index][c_index]
    #returns value at r_index and c_index
    #raises IndexError if index out of bounds
    l.print()
    #prints the list
    l.remove(r_index, c_index)
    #removes the value at r_index and c_index
    #returns true if removed, false if index out of bounds
    item in l
    #returns true if item in l, false otherwise
    l.index(item)
    #returns indices of item if found in list
    #returns [-1] otherwise
    l.__len__() / len(l)
    #returns the length of l
    l.__str__() / str(l)
    #returns l as a str
    l.__delitem__(key) / del l[key]
    #deletes row key from l
    #raises IndexError if key out of bounds

RaggedList Class
                

Creates a 2D list, but doesn't need to be of n x n size, inherits from
List2D, and therefore has a dependency to
influence.extender.list.multilist

Importing:

.. code:: py

    from influence.list import ragged
    #or
    from influence.list.ragged import RaggedList

Initializing:

.. code:: py

    r = RaggedList(rows=1, cols=1)
    #creates a ragged list starting with rows rows and cols cols
    #defaults to one for both if no arguments are given

Methods:

.. code:: py

    r.print()
    #prints the ragged list
    r.in_bounds(r_index, c_index)
    #returns true if r_index and c_index are in bounds of the list
    #returns false otherwise
    r.set(r_index, c_index, item)
    #sets value at r_index and c_index to item if in bounds
    #else extends the ragged list so r_index and c_index are in bounds
    r.get(r_index, c_index)
    #returns value at r_index and c_index if in bounds
    #else returns None
    item in r
    #returns true if item is in r, else returns false
    r.index(item)
    #returns the indices of item if in r
    #else returns [-1]
    r.__len__() / len(r)
    #returns the length of r

AsList Class
            

Used to turn strings into lists, duplicate class found in string
subpackage

Importing:

.. code:: py

    from influence.list import aslist
    #or
    from influence.list.aslist import AsList

Methods:

.. code:: py

    AsList.character_list(string)
    #returns string as a list of characters
    AsList.word_list(string)
    #returns string as a list with each word
    #a word is found when a space is reached in the string
    #spaces are not included in the list
    AsList.word_list_with_spaces(string)
    #same as AsList.word_list(string) except spaces are part of the list

AsList Class
            

Used to turn strings into lists, duplicate class found in list
subpackage

Importing:

.. code:: py

    from influence.string import aslist
    #or
    from influence.string.aslist import AsList

Methods:

.. code:: py

    AsList.character_list(string)
    #returns string as a list of characters
    AsList.word_list(string)
    #returns string as a list with each word
    #a word is found when a space is reached in the string
    #spaces are not included in the list
    AsList.word_list_with_spaces(string)
    #same as AsList.word_list(string) except spaces are part of the list

Subtract Class
              

Allows for subtracting of strings, but does not change the input string,
instead returns a new string

Importing:

.. code:: py

    from influence.string import subtract
    #or
    from influence.string.subtract import Subtract

Methods:

.. code:: py

    Subtract.subtract(initial, remove)
    #removes the first instance of remove from initial
    #returns a new string
    #remove can be multiple letters, but must be a string
    Subtract.subtract_all(initial, remove)
    #removes all instances of remove from initial
    #returns a new string
    #remove can be multiple letters, but must be a string

Const Class
===========

Gives the user access to constants in math

Importing:

.. code:: py

    from influence.math import const
    #or
    from influence.math.const import MathConstants

Fields:

.. code:: py

    MathConstants.pi #returns the value of pi
    MathConstants.e #returns the value of e
    MathConstants.tau #returns the value of tau
    MathConstants.phi #returns the value of phi

Stats Class
           

Allows for statistics with int or float datasets

Importing:

.. code:: py

    from influence.math import stats
    #or
    from influence.math.stats import Stats

Methods:

.. code:: py

    Stats.min(dataset)
    #returns the lowest value in dataset
    Stats.max(dataset)
    #returns the highest value in dataset
    Stats.range(dataset)
    #returns the range of the dataset (max - min)
    Stats.mean(dataset)
    #returns the mean of the dataset
    Stats.variance(dataset)
    #returns the variance of the dataset
    Stats.standard_deviation(dataset)
    #returns the standard deviation of the dataset
    Stats.median(dataset)
    #returns the median of the dataset
    Stats.mode(dataset)
    #returns the mode of the dataset as a list

Cos Class
         

Does permutations and combinations equations, inherits from Stats, and
therefore has a dependency to influence.extender.math.stats

Importing:

.. code:: py

    from influence.math import cos
    #or
    from influence.math.cos import Combinatorics

Methods:

.. code:: py

    Combinatorics.factorial(num)
    #returns the factorial of num
    Combinatorics.P(n, r)
    #returns the permutations equation (n! / (n-r)!)
    Combinatorics.C(n, r)
    #returns the combinations equation (n! / [(n-r)! * r!])

Frac Class
          

Represents a fraction

Importing:

.. code:: py

    from influence.math import frac
    #or
    from influence.math.frac import Fraction

Initializing:

.. code:: py

    f = Fraction(num, denom)
    #initializes a fraction to numerator num and denominator denom

Methods:

.. code:: py

    f.simplify()
    #simplifies this fraction, if possible
    f.__float__() / float(f)
    #returns the float value of the fraction
    f.__int__() / int(f)
    #returns the int value of the fractions
    f.__str__() / str(f)
    #returns the fraction as a string
    f.to_mixed_number(self)
    #returns f as a mixed number

Compare:

.. code:: py

    f1 = Fraction(1, 2)
    f2 = Fraction(3, 4)
    #fraction allows for
    f1 < f2
    f1 <= f2
    f1 == f2
    f1 > f2
    f1 >= f2

MixedNum Class
              

Represents a mixed number

Importing:

.. code:: py

    from influence.math import mixednum
    #or
    from influence.math.mixednum import MixedNumber

Initializing:

.. code:: py

    m = MixedNumber(coeff, num, denom)
    #creates a mixed number with a coefficient coeff, numerator num
    #and denominator denom

Methods:

.. code:: py

    m.simplify()
    #simplifies this mixed number, if possible
    m.__float__() / float(m)
    #returns the float value of the mixed number
    m.__int__() / int(m)
    #returns the int value of the mixed number
    m.__str__() / str(m)
    #returns the mixed number as a str
    m.to_fraction()
    #returns the mixed number as a new improper fraction

Compare:

.. code:: py

    m1 = MixedNumber(1, 2, 3)
    m2 = MixedNumber(4, 5, 6)
    #fraction allows for
    m1 < m2
    m1 <= m2
    m1 == m2
    m1 > m2
    m1 >= m2

Grapher Subpackage
                  

Allows for graphing equations

Importing:

.. code:: py

    from influence.math.grapher import Equation
    from influence.math.grapher import GraphingError
    from influence.math.grapher import Grapher

Equation Class:

Represents an equation

Initializing:

.. code:: py

    e = Equation(eq)
    #eq cannot be inferred
    #ie 4x+3 needs to be 4*x+3
    #ie 4x^2+2 needs to be 4*(x**2)+3

GraphingError Class:

GraphingError.HostileAttackError is thrown when a hostile attack is
detected with eval GraphingError.InstanceError is thrown when graphing,
the parameter is not an instance of Equation

Grapher Class:

.. code:: py

    Grapher.graph(eq)
    #graphs eq, if and only if isinstance(eq, Equation) returns True

Agrapher Subpackage
                   

Asynchronous graphing is currently a WIP but are still able to be used

Importing:

.. code:: py

    from influence.math.asyncgrapher import Equation
    from influence.math.asyncgrapher import GraphingError
    from influence.math.asyncgrapher import Grapher

Agrapher works in the same exact way except Grapher.graph(eq,
timetoclose=None), can have a given timeout

Array Class
           

Makes an array. An array is like a list, except it has a definite,
unchangeable size, but elements can be changed inside of it (unlike a
tuple)

Importing:

.. code:: py

    from influence.array import arrays
    #or
    from influence.array.arrays import Array

Initializing:

.. code:: py

    arr = Array(capacity)
    #initializes the array to its definite length 

Methods:

.. code:: py

    arr[index]
    #gets the value at index
    arr[start:stop:step]
    #returns a list from an array from a slice of start, stop, and step
    #raises IndexError if index out of bounds
    arr[index] = item
    #sets the value at index to item
    #raises IndexError if index out of bounds
    arr.__iter__() / iter(arr)
    #returns an iterator for the array
    iterator.__next__() / next(iterator)
    #gets the next element from the iterator
    arr.print()
    #prints the array
    item in arr
    #returns true if item is in arr, false otherwise
    arr.index(item)
    #returns the index of item if in arr
    #returns -1 if not found
    arr.__len__() / len(arr)
    #returns the length of arr
    not arr
    #returns True if arr has a capacity of 0
    arr.__str__() / str(arr)
    #returns arr as a str
    arr1 + arr2
    arr1 += arr2
    #adds the arrays together

Array2D Class
             

Creates a 2D Array, inherits from Array, and therefore has a dependency
to influence.upgrader.array.arrays

Importing:

.. code:: py

    from influence.array import multiarray
    #or
    from influence.array.multiarray import Array2D

Initializing:

.. code:: py

    arr = Array2D(r, c)
    #creates a 2D array to a fixed amount of rows (r) and columns (c)

Methods:

.. code:: py

    arr[r_index][c_index]
    #returns the value at r_index and c_index
    #raises IndexError if index out of bounds
    arr[r_index][c_index] = item
    #sets value at r_index and c_index to item
    #raises IndexError if index out of bounds
    arr.print()
    #prints the 2D array
    item in arr
    #returns true if item is in arr, false otherwise
    arr.index(item)
    #returns the indices of item in arr, if found
    #returns [-1] otherwise
    arr.__len__() / len(arr)
    #returns length of arr

StringBuffer Class
                  

Makes strings mutable, like in java

Importing:

.. code:: py

    from influence.string import stringbuffer
    #or
    from influence.string.stringbuffer import StringBuffer

Initializing:

.. code:: py

    s = StringBuffer(str='')
    #initializes a string buffer to str, empty if none entered

Methods:

.. code:: py

    s.__len__() / len(s)
    #returns the length of s
    obj in s
    #returns true if obj is in s, false otherwise
    s.__iter__() / iter(s)
    #returns an iterator for s
    s.__next__() / next(s)
    #gets next letter in s
    s.__str__() / str(s)
    #gets s as a normal string
    s[index]
    #gets letter at index
    s[start:stop:step]
    #gets letters starting at start, up to but discluding stop, incrementing by step
    s[index] = item
    #sets letter at index to item
    s.append(append)
    #appends append to s
    s.index(obj)
    #returns the index of obj in s
    s.insert(index, obj)
    #inserts obj at index
    s.replace(start, stop, obj)
    #replaces the chars from stop to stop (discluding stop) with obj
    del s[index]
    #deletes the char at index
    s1 + s2
    s1 += s2
    #adds stringbuffers together

Stack Class
           

Represents a stack of items, top being the newest, and bottom being the
oldest

Importing:

.. code:: py

    from influence.list import stack
    #or
    from influence.list.stack import Stack

Initializing:

.. code:: py

    s = Stack()
    #creates an empty stack

Methods:

.. code:: py

    s.push(obj)
    #puts an item to the top of the stack
    s.pop()
    #removes the top item in the stack
    #raises stack.EmptyStackError if stack is empty
    s.peek()
    #gets the top item in the stack without removing it
    #returns None if stack is empty
    s.empty()
    #returns True if s is empty
    obj in s
    #returns True if obj is in s, False otherwise
    s.index(obj)
    #returns the index of obj, -1 if not found
    s.__len__() / len(s)
    #returns the length of s
    s.__str__() / str(s)
    #returns s as a str

InsertableDict Class
                    

A dict which can insert items at a certain index

Importing:

.. code:: py

    from influence.dict import idict
    #or
    from influence.dict.idict import InsertableDict

Initializing:

.. code:: py

    i = InsertableDict()
    #creates an empty insertable dict

Methods:

.. code:: py

    i[key]
    #gets the value from i of key key
    i[key] = item
    #sets the value at key to item
    #or creates a new key and value if key not in i
    i.__len__() / len(i)
    #gets the length of i
    i.get(key)
    #like i[key] but returns None if key is not in i
    i.append(key, item)
    #appends key and item to the end of the i
    i.keys()
    #returns the keys of i
    i.values()
    #returns the values of i
    i.__str__() / str(i)
    #returns i as a str
    i.remove(key)
    #removes the key and value of key
    i.pop()
    #removes the last element in i
    i.__iter__() / iter(i)
    #returns an iter object for i
    i.__next__() / next(i)
    #returns the next element in i
    i.insert(index, key, value)
    #inserts key and value at index (index starts at 0)

TreeSet Class
             

A normal set (where you can't have duplicate items), except all items
are automatically sorted upon adding

Importing:

.. code:: py

    from influence.set import treeset
    #or
    from influence.set.treeset import TreeSet

Initializing:

.. code:: py

    ts = TreeSet(t)
    #creates a treeset that takes in values of type t

Methods:

.. code:: py

    ts.add(item)
    #adds item to ts and sorts the set
    #raises ValueError if item is not of instance t
    #returns True if added, False if item already in set
    obj in ts
    #returns True if obj is in ts, False otherwise
    ts.remove(item)
    #removes item from ts
    #raises an error if item not in ts
    ts.discard(item)
    #removes item from ts if found
    #does not raise an error if not found
    ts.__len__() / len(ts)
    #returns the length of ts
    ts.__str__() / str(ts)
    #returns ts as a str
    ts.__iter__() / iter(ts)
    #returns an iterator for ts
    ts.__next__() / next(ts)
    #returns the next element in ts
    ts.pop()
    #removes the last element in ts

TreeMap Class
             

A normal dictionary, except items are automatically sorted by key from
least to greatest

Importing:

.. code:: py

    from influence.dict import treemap
    #or
    from influence.dict.treemap import TreeMap

Initializing:

.. code:: py

    tm = TreeMap()
    #initializes an empty treemap

Methods:

.. code:: py

    tm.add(key, value)
    #adds key and value to tm and sorts the dict
    obj in tm
    #returns True if obj is in tm.keys() or tm.values(), False otherwise
    tm.keys()
    #returns the keys in tm
    tm.values()
    #returns the values in tm
    tm.__str__() / str(tm)
    #returns tm as a str
    tm.remove(key)
    #removes the key and value of key from tm
    tm.pop()
    #removes the last element key and value from tm
    tm.__len__() / len(tm)
    #returns the length of tm
    tm.__iter__() / iter(tm)
    #returns an iterator for tm
    tm.__next__() / next(tm)
    #returns the next element in tm

StemLeaf Class
              

Creates a stem and leaf plot

Importing:

.. code:: py

    from influence.math import stemandleaf
    #or
    from influence.math.stemandleaf import StemLeaf

Initializing:

.. code:: py

    sl = StemLeaf()
    #initializes an empty stem and leaf plot

Methods:

.. code:: py

    sl.plot(stem, leaf)
    #adds the stem and leaf to plot
    sl.remove(stem, leaf)
    #removes the leaf from the given stem if found
    #raises stemandleaf.NoStemError if stem not found
    #raises stemandleaf.NoLeafError if leaf not found in stem
    sl.__str__() / str(sl)
    #returns sl as a str
    sl.empty()
    #returns True if sl is empty, False otherwise

License
=======

MIT License

Copyright (c) 2020 RandomKiddo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
