#!/usr/bin/env python

__author__ = 'Marc Schwarzschild'

from strongdict import StrongDict, memo, memo_until, nmemo

def test_simple():
  'Testing strong dictionary.'
  v = StrongDict()
  v['One'] = 1
  v[2] = 2
  v['Three'] = 'Three'

  assert v['One'] == 1
  assert v[2] == 2
  assert v['One'] == 1
  assert v['Three'] == 'Three'

  return

def test_iteritems():
  '''Testing iteritems'''
  w = StrongDict()
  w['One'] = 1
  w[2] = 2
  w['Three'] = 'Three'
  x = {}
  for k, v in w.iteritems(): x[k] = v
  y = {2: 2, 'Three': 'Three', 'One': 1}
  assert(x == y)


def test_instantiation():
  data = {2: 2, 'Three': 'Three', 'One': 1}
  v = StrongDict(data)
  assert str(data) == str(v)
  w = StrongDict(v)
  assert str(v) == str(w)
  return

def test_n_limit():
  w = StrongDict(limit=3)
  for i in range(10): w[i] = i * i
  assert(len(w) == 3)
  assert(6 not in w)
  del w[8]
  assert(len(w) == 2)
  try:
    del w[6]
    assert(False)
  except KeyError:
    'It cannot delete w[7] since it is not there.'
    assert(True)
    
  del w[9]
  assert(9 not in w)

  x = {}
  for i in range(4):
    w[i] = x[i]= i * i
  del x[0]
  assert(w == x)

def test_time_limit():
  from time import sleep
  w = StrongDict(tlimit=2)
  w[1] = 'One'
  sleep(1)
  w['Two'] = 2
  x ={1:'One', 'Two':2}
  assert(x == w)
  sleep(1)
  w['Three'] = 'Three'
  sleep(1)
  x = {'Three':'Three'}
  assert(w == x)
  sleep(3)
  assert(len(w) == 0)
 
def test_retention():
  import gc
  '''Test if weak reference forget objects deleted from the cache.'''

  limit = 3
  w = StrongDict(limit=limit)
  n = 50
  for i in range(n):
    x = [1]
    w[i] = x
  x = None
  assert(limit == len(w))
  w.clear()
  assert(0 == len(w))

  # w.weak_len() could be non zero depending on garbage collection activity.
  assert (w.weak_len() <= limit)

  gc.collect()
  assert(0 == w.weak_len())

class TestMemoFlag(object):
  def __init__(self): self.__flag = False
  def __call__(self, f): self.__flag = True if f else False
  def __eq__(self, f): return self.__flag == f

def test_memo():
  '''
    Test @memo decorator.
    Memoized foo() only executes for new values of x.
  '''

  tmf = TestMemoFlag()

  @memo
  def foo(x):
    tmf(True) # will only execute if value of x is used for the first time.
    return x

  foo(1)
  assert(True == tmf)

  tmf(False)
  foo(2)
  assert(True == tmf)

  tmf(False)
  foo(1)
  assert(False == tmf)  # arg 1 should be remembered so tmf will be false.

def test_memo_until():
  '''
    Test @memo_until decorator.
    Memoized foo() only executes for new values of x or if time limit expired.
  '''
  from time import sleep

  tmf = TestMemoFlag()

  @memo_until(tlimit=1)
  def foo(x):
    tmf(True) # will only execute if value of x is used for the first time.
    return x

  foo(1)
  assert(True == tmf)

  tmf(False)
  foo(1)
  assert(False == tmf)

  sleep(2)
  tmf(False)
  foo(1)
  assert(True == tmf)

  tmf(False)
  foo(1)
  assert(1 == foo('size_elephant_cache'))
  foo('clear_elephant_cache')
  tmf(False)
  foo(1)
  

def test_nmemo():
  '''
    Test @nmemo decorator.
  '''
  tmf = TestMemoFlag()

  @nmemo(3)
  def foo(x):
    tmf(True) # will only execute if value of x is used for the first time.
    return x

  tmf(False)
  foo(1)
  assert(True == tmf)

  tmf(False)
  foo(2)
  assert(True == tmf)

  tmf(False)
  foo(1)
  assert(False == tmf)

  tmf(False)
  foo(3)
  assert(True == tmf)

  tmf(False)
  foo(4)
  assert(True == tmf)

  tmf(False)
  foo(5)
  assert(True == tmf)

  tmf(False)
  foo(6)
  assert(True == tmf)

  tmf(False)
  foo(1)
  assert(True == tmf)

  assert(3 == foo('size_elephant_cache'))
  

if __name__ == "__main__":
  import sys

  usage = '''
  Run one of the nose tests listed below using the command shown.

  Run one of the nose test methods in a debugger by invoking this module with
  the nose test method as the argument.

  $ pdb test_strongdict.py test_simple

  '''

  print usage

  for i in dir():
    if i.startswith('test'):
      print 'nosetests -s', __file__ + ':' + i

  print

  if len(sys.argv) > 1:
    f_name = sys.argv[1]
    try:
      f = globals()[f_name]
      print 'About to run', f_name, '...'
      f()  # Set breakpoint here in debugger to step into given method.
    except KeyError:
      print 'Could not find named method.'
  else:
    print 'Usage:', __file__, '[method]'
