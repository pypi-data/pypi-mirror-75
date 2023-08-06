from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='gexecute',
    version='0.0.5',
    author='Tim Cosby',
    author_email='tim470773@gmail.com',
    url='https://github.com/TimCosby/generic_execute',
    description='Generically execute any function with a unknown function, module, or set of parameters!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['gexecute'],
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    keywords='generic execute function module',
)
