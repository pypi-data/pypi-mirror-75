from setuptools import setup, find_packages

setup(
  name = 'electra-pytorch',
  packages = find_packages(),
  version = '0.0.1',
  license='MIT',
  description = 'Electra - Pytorch',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/electra-pytorch',
  keywords = ['transformers', 'artificial intelligence', 'pretraining'],
  install_requires=[
      'torch'
  ],
  classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
  ],
)