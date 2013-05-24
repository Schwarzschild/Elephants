from distutils.core import setup

with open('README.rst', 'r') as fh:  txt = fh.read()
with open('LICENSE.txt', 'r') as fh:  lic = fh.read()
script = "s = '''\n" + txt + '\n' + lic + "\n'''\n\ndef readme(): return s"
with open('elephants/readme.py', 'w') as fh: fh.write(script)

setup(
  name='Elephants',
  version='0.1.1',
  author='Marc Schwarzschild',
  author_email='ms@TheBrookhavenGroup.com',
  url='http://github.com/Schwarzschild/Elephants',
  license='MIT',
  description='Memoization utilities with fading memory.',
  keywords=['memo', 'memoize', 'cache'],
  packages=['elephants',],
)
