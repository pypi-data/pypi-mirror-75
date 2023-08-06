from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='relocate',
      version='2.0.0',
      license='MIT',
      author='Sandip Palit',
      author_email='sandippalit009@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='Relocate is a Python Package by Sandip Palit. It will help you in organising your files into distinct folders.',
      packages=['relocate'],
      python_requires='>=3.6',
      zip_safe=False)