from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
  name='CSGOMemPy',
  version='1.0.0',
  description='Easy to use CSGO mod functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='EthanEDITS',
  author_email='ethaneditsbusiness@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='csgo memory windows', 
  packages=find_packages(),
  install_requires=['Pymem'] 
)