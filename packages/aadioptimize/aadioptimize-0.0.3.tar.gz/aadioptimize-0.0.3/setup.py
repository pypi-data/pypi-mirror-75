from setuptools import setup

setup(
    name="aadioptimize",
    version='0.0.3',
    description='Perform optimization for function',
    url='https://github.com/aaditep/aadioptimize',
    author='Aadi Tepper',
    author_email='aaditep@gmail.com',
    licence='MIT',
    packages=['aadioptimize','funcs'],
    install_requires=[
        'numpy'
    ],
    python_requires='>=3.7'
)

