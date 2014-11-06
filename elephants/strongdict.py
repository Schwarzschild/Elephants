#!/usr/bin/env python

__author__ = 'Marc Schwarzschild'

# import os
# p = os.path.dirname(os.path.abspath(__file__))
# __doc__ = open(os.path.join(p, 'README.md')).read()

future_notes = '''
  strongdict.py - memoization with strong and weak references

  Future: Make the cache thread safe by holding the GIL using mutex.
'''

import weakref
from functools import wraps
from datetime import datetime, timedelta

class Link(object):
  #  Slots are not compatible with WeakValueDictionary
  def __init__(self, data, b=None, a=None):
    self.data = data
    self.before = b
    self.after = a
    self.t = datetime.now()

  def __str__(self): return str(self.data)
  __repr__ = __str__

  def print_all(self): print self.before, '->', self, '->', self.after

class StrongDict(object):
  '''
     A dictionary using strong and weak references.

     See ../README.md
  '''     

  def __init__(self, data=None, limit=None, tlimit=None, **kwargs):
    self.__weak_cache = weakref.WeakValueDictionary()
    self.strong_cache = None
    self.strong_cache_end = None
    self.n = 0
    self.limit = limit
    self.tlimit = timedelta(seconds=tlimit) if tlimit else None
    if data: self.extend(data)
    if len(kwargs): self.extend(kwargs)

  def __to_dict(self):
    # Make sure not to use iteritems() because it updates item times and order.
    return dict([(k, v) for k, v in self.iteritems_no_update()])

  def __repr__(self): return repr(self.__to_dict())
  __str__ = __repr__
  def __unicode__(self): return unicode(self.__str__())

  __hash__ = None # Avoid Py3k warning

  def __is_in_strong_cache(self, l):
    return (l.before != l.after) or \
           (self.strong_cache == l) or \
           (self.strong_cache_end == l)
           
  def __add_to_top_of_strong_cache(self, l):
    top = self.strong_cache
    if top is None:
      self.strong_cache = self.strong_cache_end = l
      l.after = l.before = None
      self.n = 1
    else:
      l.before = None
      l.after = top
      top.before = l
      self.strong_cache = l
      self.n += 1

  def __remove_last_item_from_strong_cache(self):
    n = self.n
    if not n: return
    if 1 == n:
      self.clear()
    else:
      bottom = self.strong_cache_end
      self.strong_cache_end = bottom.before
      self.strong_cache_end.after = None
      self.n -= 1

  def __add_to_strong_cache(self, l):
    if self.tlimit: l.t = datetime.now()
    if self.limit and (self.n == self.limit):
      self.__remove_last_item_from_strong_cache()
      self.__add_to_top_of_strong_cache(l)
    else:
      self.__add_to_top_of_strong_cache(l)

  def __move_to_beginning(self, l):
    if self.tlimit: l.t = datetime.now()
    if not self.__is_in_strong_cache(l):
      # It must have been found in the weak cache by __contains__().      
      self.__add_to_strong_cache(l)
    elif l.before:
      top = self.strong_cache
      if l == top: return

      after = l.after
      before = l.before

      # before -> l -> after
      before.after = after
      if after: after.before = before

      l.before = None
      l.after = top
      top.before = l
      self.strong_cache = l
      if self.strong_cache_end == l: self.strong_cache_end = before

  def __setitem__(self, k, v):
    w = self.__weak_cache
    try:
      l = w[k]
      l.data = (k, v) # may be updating v
      self.__move_to_beginning(l)
    except KeyError:
      l = Link((k, v))
      w[k] = l
      self.__add_to_strong_cache(l)

  def __remove_expired_item(self, l):
    tlimit = self.tlimit
    if tlimit:
      t_now = datetime.now()
      if tlimit and (t_now - l.t > tlimit): del self[l.data[0]]

  def __getitem__(self, k):
    try:
      l = self.__weak_cache[k]
    except KeyError:
      raise KeyError, k
    self.__remove_expired_item(l)
    if not self.__is_in_strong_cache(l): raise KeyError, k
    self.__move_to_beginning(l)
    return l.data[1]

  def __delitem__(self, k):
    if type(k) is Link:
      l = k
    else:
      try:
        l = self.__weak_cache[k]
      except KeyError:
        raise KeyError, k

    if l.after and l.before:
      l.before.after = l.after
      l.after.before = l.before
      self.n -= 1
    elif l.before:
      self.strong_cache_end = l.before
      self.n -= 1
    elif l.after:
      self.strong_cache = l.after
      self.n -= 1
    elif (1 == self.n) and (self.strong_cache == l):
      self.strong_cache = self.strong_cache_end = None
      self.n = 0

    l.before = l.after = None
      
  def weak_len(self): return len(self.__weak_cache)
  def __len__(self): 
    if self.tlimit: self.keys() # keys() will check all item times
    return self.n

  def __contains__(self, k):
    try:
      l = self.__weak_cache[k]
    except KeyError:
      return False
    self.__remove_expired_item(l)
    if not self.__is_in_strong_cache(l): return False
    return True

  def keys(self):
    l = self.strong_cache
    result = []
    while l:
      after = l.after
      self.__remove_expired_item(l)
      if self.__is_in_strong_cache(l): result.append(l.data[0])
      l = after
    return result

  def __eq__(self, x):
    b = dict(x)
    a = dict(self)
    return a == b
    return dict(self) == dict(x)

  def iteritems_no_update(self):
    # Do not use self[k] to access items because it will update item times.
    l = self.strong_cache
    while l:
      after = l.after
      self.__remove_expired_item(l)
      if self.__is_in_strong_cache(l):
        k, v = l.data
        yield k, v
      l = after

  def iteritems(self):
    for k in self.keys():
      try:
        yield k, self[k]
      except:
        pass
      
  def extend(self, data):
    if type(data) is StrongDict:
      for k, v in data.iteritems_no_update(): self[k] = v
    else:
      for k, v in data.iteritems(): self[k] = v

  def clear(self):
    self.strong_cache = self.strong_cache_end = None
    self.n = 0

  def clear_weak(self):
    self.__weak_cache = weakref.WeakValueDictionary()

  def copy(self): return StrongDict(self)

  # SHOULD ONLY BE USED FOR UNIT TESTS IN THIS PACKAGE.
  def _get_weak_cache(self): return self.__weak_cache

# Ideas from 'Python Algorithms' by Mangus Lie Hetland, Apress 2010,
# ISBN 978-1-4302-3237-7, page 177
def memoizer(f, tlimit=None, limit=None):
  cache = StrongDict(tlimit=tlimit, limit=limit)
  @wraps(f)  # Makes the wrap function think it has the name of f.
  def wrap(*args, **kwargs):
    if len(args):
      x = args[0]
      if (type(x) is str):
        if 'clear_elephant_cache' == x:
          cache.clear()
          cache.clear_weak()
          return x
        elif 'size_elephant_cache' == x:
          return len(cache)

    k = (args, tuple(kwargs.items()))
    try:
      return cache[k]
    except KeyError:
      x = f(*args, **kwargs)
      cache[k] = x
      return x
  return wrap

def memo(f): return memoizer(f)

def memo_until(tlimit):
  def real_memo(f): return memoizer(f, tlimit=tlimit)
  return real_memo

def nmemo(limit):
  def real_memo(f): return memoizer(f, limit=limit)
  return real_memo

