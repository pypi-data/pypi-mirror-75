from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyit2fls',
      version='0.5',
      description='Interval Type 2 Fuzzy Logic Systems in Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Haghrah/PyIT2FLS',
      author='Amir Arslan Haghrah',
      author_email='arslan.haghrah@gmail.com',
      license='MIT',
      packages=['pyit2fls'],
      install_requires=['numpy', 'matplotlib', ],
      python_requires='>=3.6',
      zip_safe=False)
