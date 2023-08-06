from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='distributions_harsh',
      version='0.1',
      description='Gaussian and Binomial distributions',
      packages=['distributions_harsh'],
      author='Harsh Bhandari',
      author_email='harshbhandari32@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
