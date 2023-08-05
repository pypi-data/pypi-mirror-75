from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='moreFunctions',
    version='1.0.2',
    description='A compilation of additional functions for use in varying purposes in Python',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Rac Elizaga',
    author_email='rac_elizaga@yahoo.com',
    license='MIT',
    classifiers=classifiers,
    keywords='functions',
    packages=find_packages(),
    install_requires=['']
)
