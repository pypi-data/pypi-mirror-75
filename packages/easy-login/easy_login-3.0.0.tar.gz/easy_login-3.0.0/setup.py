from setuptools import setup




with open("README.md", "r") as fh:
    long_description = fh.read()




setup(name='easy_login',
      version='3.0.0',
      author="vasu_gupta",
      description='Logging social accounts automatically using python package',
      long_description=long_description,
      url="https://github.com/vasu04gupta/log_in",
      packages=['easy_login'],classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],zip_safe=False)


