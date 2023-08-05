from setuptools import setup,find_packages

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name='elutils',
    version='0.0.5',
    description='A small package of my utities',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Emil Elgaard',
    author_email='shivan@shivan.dk',
    license='MIT',
    classifiers=classifiers,
    keywords='utilities',
    packages=find_packages(),
    install_requires=['']
)