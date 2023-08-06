
import setuptools

with open('README.md', 'r') as rdm:
    long_description = rdm.read()

setuptools.setup(
    name='ajsum',
    version='0.0.2',
    author='Alex Summers',
    author_email='ajsummers7@gmail.com',
    description='A small package for convenient functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ajsummers/ajsum',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
