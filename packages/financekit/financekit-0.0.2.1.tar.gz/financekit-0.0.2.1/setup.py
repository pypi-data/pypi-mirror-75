import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='financekit',
      version='0.0.2.1',
      description='A financial package for Python',
      long_description=long_description,
      url='https://github.com/GuillaumeKark/financekit',
      author='Guillaume Karklins',
      author_email='guillaume.karklins_marchay@edu.escp.eu',
      license='Apache License 2.0',
        classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"],
      packages=setuptools.find_packages())
