Influence - The Python Extender You Asked For
=============================================

With influence you can extend python with things like two-dimensional lists, fractions, string
subtractors, etc. You can also upgrade python with things it doesn’t have like arrays!

Overview
========

The influence python library was created with one sole purpose, helping you do things that can’t be
done in standard python with ease

-  Extender Library: Sub-package of influence that extends things that are already in python, such
   as lists, strings, and doing math
-  Upgrader Library: Sub-package of influence that adds things to python that it doesn’t have
   already, like arrays

Usage
=====

Below is how to install and use the influence library in your own programs!

Installation
------------

.. code:: sh

   $ pip install influence
   or 
   $ python3 -m pip install -U influence

The influence package has two package dependencies, numpy and matplotlib (used for grapher and
agrapher classes)

Extender Library
----------------

The influence subpackage that extends python’s built-in features

Cout
~~~~

Cout (common output) has only one module, printer, that helps print tuples, lists, dicts, etc.
nicely

Importing:

.. code:: py

   from influence.extender.cout import printer
   #or
   from influence.extender.cout.printer import Printer

Printer Class
^^^^^^^^^^^^^

Methods:

.. code:: py

   Printer.print_list(list) #prints a list nicely
   Printer.print_tuple(tuple) #prints a tuple nicely
   Printer.print_dictionary(dict) #prints a dict nicely
   Printer.print_all(ender, *items) 
   #prints all of items, if ender is False, prints each item on new line
   #else all items are printed on the same line

List
~~~~

List extends python’s built-in lists by adding multidimensional lists and other list extenders

List2D Class
^^^^^^^^^^^^

Creates a 2D list of a square size

Importing:

.. code:: py

   from influence.extender.list import multilist
   #or
   from influence.extender.list.multilist import List2D

Initializing:

.. code:: py

   l = List2D(rows, cols) 
   #creates the list to have rows number of rows and cols number of cols

Methods:

.. code:: py

   l.set(r_index, c_index, item)
   #sets value at r_index and c_index to item
   #returns true if able to set, false if index out of bounds
   l.get(r_index, c_index)
   #returns value at r_index and c_index
   #returns None if index out of bounds
   l.print()
   #prints the list
   l.remove(r_index, c_index)
   #removes the value at r_index and c_index
   #returns true if removed, false if index out of bounds
   item in l
   #returns true if item in l, false otherwise
   l.find(item)
   #returns indices of item if found in list
   #returns [-1] otherwise

RaggedList Class
^^^^^^^^^^^^^^^^

Creates a 2D list, but doesn’t need to be of n x n size, inherits from List2D, and therefore has a
dependency to influence.extender.list.multilist

Importing:

.. code:: py

   from influence.extender.list import ragged
   #or
   from influence.extender.list.ragged import RaggedList

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
   r.find(item)
   #returns the indices of item if in r
   #else returns [-1]

AsList Class
^^^^^^^^^^^^

Used to turn strings into lists, duplicate class found in string subpackage

Importing:

.. code:: py

   from influence.extender.list import aslist
   #or
   from influence.extneder.list.aslist import AsList

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

String
~~~~~~

Allows for a couple new things to be done with strings

.. _aslist-class-1:

AsList Class
^^^^^^^^^^^^

Used to turn strings into lists, duplicate class found in list subpackage

Importing:

.. code:: py

   from influence.extender.string import aslist
   #or
   from influence.extneder.string.aslist import AsList

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
^^^^^^^^^^^^^^

Allows for subtracting of strings, but does not change the input string, instead returns a new
string

Importing:

.. code:: py

   from influence.extender.string import subtract
   #or
   from influence.extender.string.subtract import Subtract

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

Math
~~~~

#Const Class

Gives the user access to constants in math

Importing:

.. code:: py

   from influence.extender.math import const
   #or
   from influence.extender.math.const import MathConstants

Fields:

.. code:: py

   MathConstants.pi #returns the value of pi
   MathConstants.e #returns the value of e
   MathConstants.tau #returns the value of tau
   MathConstants.phi #returns the value of phi

Stats Class
^^^^^^^^^^^

Allows for statistics with int or float datasets

Importing:

.. code:: py

   from influence.extender.math import stats
   #or
   from influence.extender.math.stats import Stats

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
^^^^^^^^^

Does permutations and combinations equations, inherits from Stats, and therefore has a dependency to
influence.extender.math.stats

Importing:

.. code:: py

   from influence.extender.math import cos
   #or
   from influence.extender.math.cos import Combinatorics

Methods:

.. code:: py

   Combinatorics.factorial(num)
   #returns the factorial of num
   Combinatorics.P(n, r)
   #returns the permutations equation (n! / (n-r)!)
   Combinatorics.C(n, r)
   #returns the combinations equation (n! / [(n-r)! * r!])

Frac Class
^^^^^^^^^^

Represents a fraction

Importing:

.. code:: py

   from influence.extender.math import frac
   #or
   from influence.extender.math.frac import Fraction

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
^^^^^^^^^^^^^^

Represents a mixed number

Importing:

.. code:: py

   from influence.extender.math import mixednum
   #or
   from influence.extender.math.mixednum import MixedNumber

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
^^^^^^^^^^^^^^^^^^

Allows for graphing equations

Importing:

.. code:: py

   from influence.extender.math.grapher.grapher import Equation
   from influence.extender.math.grapher.grapher import GraphingError
   from influence.extender.math.grapher.grapher import Grapher

Equation Class:

Represents an equation

Initializing:

.. code:: py

   e = Equation(eq)
   #eq cannot be inferred
   #ie 4x+3 needs to be 4*x+3
   #ie 4x^2+2 needs to be 4*(x**2)+3

GraphingError Class:

GraphingError.HostileAttackError is thrown when a hostile attack is detected with eval
GraphingError.InstanceError is thrown when graphing, the parameter is not an instance of Equation

Grapher Class:

.. code:: py

   Grapher.graph(eq)
   #graphs eq, if and only if isinstance(eq, Equation) returns True

Agrapher Subpackage
^^^^^^^^^^^^^^^^^^^

Asynchronous graphing is currently a WIP but are still able to be used

Importing:

.. code:: py

   from influence.extender.math.agrapher.asyncgrapher import Equation
   from influence.extender.math.agrapher.asyncgrapher import GraphingError
   from influence.extender.math.agrapher.asyncgrapher import Grapher

Agrapher works in the same exact way except Grapher.graph(eq, timetoclose=None), can have a given
timeout

Upgrader Library
----------------

Array
~~~~~

Creates an array An array is like a list, except it has a definite, unchangeable size, but elements
can be changed inside of it (unlike a tuple)

Array Class
^^^^^^^^^^^

Makes an array

Importing:

.. code:: py

   from influence.upgrader.array import arrays
   #or
   from influence.upgrader.array.arrays import Array

Initializing:

.. code:: py

   arr = Array(capacity)
   #initializes the array to its definite length 

Methods:

.. code:: py

   arr.get(index)
   #gets the value at index
   #raises IndexError if index out of bounds
   arr.set(index, item)
   #sets the value at index to item
   #raises IndexError if index out of bounds
   arr.__iter__() / iter(arr)
   #returns an iterator for the array
   arr.print()
   #prints the array
   item in arr
   #returns true if item is in arr, false otherwise
   arr.find(item)
   #returns the index of item if in arr
   #returns -1 if not found

Array2D Class
^^^^^^^^^^^^^

Creates a 2D Array, inherits from Array, and therefore has a dependency to
influence.upgrader.array.arrays

Importing:

.. code:: py

   from influence.upgrader.array import multiarray
   #or
   from influence.upgrader.array.multiarray import Array2D

Initializing:

.. code:: py

   arr = Array2D(r, c)
   #creates a 2D array to a fixed amount of rows (r) and columns (c)

Methods:

.. code:: py

   arr.get(r_index, c_index)
   #returns the value at r_index and c_index
   #raises IndexError if index out of bounds
   arr.set(r_index, c_index, item)
   #sets value at r_index and c_index to item
   #raises IndexError if index out of bounds
   arr.print()
   #prints the 2D array
   item in arr
   #returns true if item is in arr, false otherwise
   arr.find(item)
   #returns the indices of item in arr, if found
   #returns [-1] otherwise

License
=======

MIT License

Copyright (c) 2020 RandomKiddo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
