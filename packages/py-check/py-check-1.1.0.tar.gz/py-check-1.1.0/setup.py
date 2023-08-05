from os import path
import json
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
print(this_directory)
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, 'package.json'), encoding='utf-8') as f:
    version = json.loads(f.read())['version']

setup(name='py-check',
      version=version,
      author='ArlenX',
      author_email='arlenxuzj@gmail.com',
      description='Python Micro check library',
      keywords='python python3 types check checker library',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/arlenxuzj/py-check',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8'
      ],
      packages=find_packages(),
      package_data={'': ['*.pyi']},
      python_requires='>=3.6, <4')
