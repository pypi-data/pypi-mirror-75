from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='pydist_prob',
      version='0.2',
      author='Elahi Concha',
      author_email='elijahshellsanchez@outlook.com',
      description='Gaussian and binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['distributions'],
      zip_safe=False)
