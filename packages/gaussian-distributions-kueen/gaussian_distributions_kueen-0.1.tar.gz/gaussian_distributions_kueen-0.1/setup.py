from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gaussian_distributions_kueen',
      version='0.1',
      description='Gaussian and Binomial distributions',
      packages=['gaussian_distributions_kueen'],
      author='Keshvi Gupta',
      author_email='keshvi2298@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
