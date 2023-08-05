from setuptools import setup

with open("gaussian_binomial_probability_distribution/README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='gaussian_binomial_probability_distribution',
      version='0.1',
      author= 'Yittyn Ng',
      author_email= 'ngyittyn980518@gmail.com',
      description='Gaussian and Binomial distribution',
      packages=['gaussian_binomial_probability_distribution'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      zip_safe=False)
