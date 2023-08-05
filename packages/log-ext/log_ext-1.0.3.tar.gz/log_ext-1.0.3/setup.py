import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='log_ext',
    version='1.0.3',
    packages=setuptools.find_packages(),
    url='https://github.com/CpHarding/py_logging_extensions',
    license='MIT License',
    author='CpHarding',
    author_email='',
    description='An extension for standard python logging',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
