s = '''
=========
Elephants
=========

This is a memoize package using StrongDict a class
introduced in this package.  StrongDict described in
detail in the following section uses a linked list of
strong references in combination with a weak reference
dictionary to enable fading memory storage by either
restricting the number of items in the store or imposing a
time limit on items stored.


About the name
--------------

This package is named Elephants because they are the symbol
of remembering, or in a modern Python world, memoizing.

Examples
--------

Simple memoize
^^^^^^^^^^^^^^

::

  from elephants import memo

  @memo
  def fib(n):
    if n<2: return 1
    return fib(n-1) + fib(n-2)

  
Memoize with time limit
^^^^^^^^^^^^^^^^^^^^^^^

The following pattern demonstrates the @memo_until
decorator to cache data object instances for a given
length of time.

::

   from elephants import memo_until

   class MyDataObject(object):
     def __init__(self, x):
       self.x = x

     def __str__(self): return str(self.x)

   @memo_until(tlimit=3600) # seconds
   def get_my_data_obj_instance(x):
     print 'Getting a new instance for x =', x
     return MyDataObject(x)


   y = get_my_data_obj_instance(1)
   y = get_my_data_obj_instance(2)
   y = get_my_data_obj_instance(1)
   y = get_my_data_obj_instance(3)
   y = get_my_data_obj_instance(1)

   print 'The final value of y should be 1.  It is', y

Memoize with length limit
^^^^^^^^^^^^^^^^^^^^^^^^^

The following pattern demonstrates the @memo_until
decorator to cache data object instances for a given
length of time.

::

   from elephants import nmemo

   class MyDataObject(object):
     def __init__(self, x):
       self.x = x

     def __str__(self): return str(self.x)

   @nmemo(limit=2) # Limit the cache to only two items.
   def get_my_data_obj_instance(x):
     print 'Getting a new instance for x =', x
     return MyDataObject(x)


   y = get_my_data_obj_instance(1)
   y = get_my_data_obj_instance(2)
   y = get_my_data_obj_instance(3)
   y = get_my_data_obj_instance(1)

   print 'At this point the cache should only have 1 and 3.'

StrongDict
^^^^^^^^^^

A dictionary using strong and weak references.

Items are stored in a WeakValueDictionary.  They are also
stored in a the linked list, the strong cache, holding
strong references.  Retreival is a fast
WeakValueDictionary lookup.  Items most recently used are
moved to the top of the strong cache list.  Options are
provided to fade from the strong linked list defined by
either a time limit or a list quantity limit.  The default
is to keep everything in strong linked list forever.  If
an item is removed from the strong cache and later queried
and found in the WeakValuedictionary it will be added back
to the strong cache.  This can only happen if an reference
to the removed item exists outside the cache.

As long as items have a strong reference they will stay in
the WeakValueDictionary.  However, if an item no longer
has a strong reference it is not guaranteed to be in the
WeakValueDictionary.  The WeakValueDictionary will
"forget" about objects not also referenced elsewhere, in
this case the StrongDict() strong reference linked list.

The weakref.WeakValueDictionary() cannot hold native types
like int or str.  But it can hold a python object that has
native types.  This StrongDict class uses a Link object
defined above to hold all values stored in the cache.
Therefore the user of StrongDict() does not need to be
concerned with this limitation of the weakref package.

CAVEAT EMPTOR: If a class instance is used as key in the
               dictionary then the __hash__() method may
               need to be implmented.

StrongDict Example
^^^^^^^^^^^^^^^^^^

::

   from elephants import StrongDict

   w = StrongDict(limit=3)

   # populate with test cases
   for i in range(10): w[i] = i * i

   # demonstrate limit is imposed and len() works for StrongDict
   assert(len(w) == 3)

   assert(6 not in w)

   # demonstrate that del works on StrongDict instances
   del w[8]
   assert(len(w) == 2)

   # demonstrate that KeyError is thrown when item is not in the dictionary.
   try:
     del w[6]
     assert(False)
   except KeyError:
     'It cannot delete w[7] since it is not there.'
     assert(True)
     
   # demonstrate for negation on inclusion test.
   del w[9]
   assert(9 not in w)

   # demonstrate equals operator
   x = {}
   for i in range(4):
     w[i] = x[i]= i * i
   del x[0]
   assert(w == x)

   # demonstrate conversion to dict
   x = dict(w)
   print x
   print type(x)


Special Note
^^^^^^^^^^^^

@memo, @nmemo, and @memo_until have two special arguments.

If a decorated method is called with
'size_elephant_cache' as the argument it will return the
number of items in the cache.  If it is called with
'clear_elephant_cache' as the argument it will clear the
cache as shown in the following example.


Example
^^^^^^^

::

   from elephants import memo

   @memo
   def f(x): return x * x

   for i in range(10): f(i)

   print 'There are', f('size_elephant_cache'), 'items in the cache.'
   f('clear_elephant_cache')
   print 'There are', f('size_elephant_cache'), 'items in the cache.'

Thank you
=========

A special thank you to Jonathan Arrender Smith for his
guidance and education.



LICENSE
=======

The MIT License (MIT)
Copyright (c) 2013 The Brookhaven Group, LLC

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall
be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


'''

def readme(): return s