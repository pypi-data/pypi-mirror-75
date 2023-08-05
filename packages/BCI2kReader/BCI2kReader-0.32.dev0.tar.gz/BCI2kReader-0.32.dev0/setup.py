from setuptools import setup

setup(
    name='BCI2kReader',
    version='0.32dev0',
    packages=['BCI2kReader',],
    license='GNU 3',
    author='Markus Adamek',
    url='https://github.com/neurotechcenter/BCI2kReader',
    author_email='adamek@neurotechcenter.com',
    install_requires=['numpy', ],
    long_description=open('README.md').read(),
    classifiers=["Development Status :: 4 - Beta",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 2"],
)