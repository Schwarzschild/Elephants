from distutils.core import setup

# Good instructions for adding a package to PyPi
#  https://jamiecurle.co.uk/blog/my-first-experience-adding-package-pypi/


with open('README.rst', 'r') as fh:  txt = fh.read()
with open('LICENSE.txt', 'r') as fh:  lic = fh.read()
script = "s = '''\n" + txt + '\n' + lic + "\n'''\n\ndef readme(): return s"
with open('elephants/readme.py', 'w') as fh: fh.write(script)

setup(
  name='Elephants',
  version='0.1.0',
  author='Marc Schwarzschild',
  author_email='ms@TheBrookhavenGroup.com',
  packages=['elephants',],
  url='http://pypi.python.org/pypi/Elephants/',
)
