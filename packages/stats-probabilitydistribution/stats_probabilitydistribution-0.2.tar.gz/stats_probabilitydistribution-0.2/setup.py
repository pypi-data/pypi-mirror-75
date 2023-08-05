from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='stats_probabilitydistribution',
      version='0.2',
      description='Gaussian & Binomial distributions',
      long_description='This package helps to calculate mean, standard deviation, Probability distribution function for Gaussian distribution and Binomial Distribution.Through the use of this package we can also plot the distribution to visualize these function and data for better understanding.Also we can Add two functions directly using method calling.',
      packages=['stats_probabilitydistribution'],
      author= 'Shubham Kumar',
      author_email= 'shubham01kumar1@gmail.com',
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
      zip_safe=False)