import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='strify',
    version='1.0.2',
    author='Eduard Konanau',
    author_email='aduard.kononov@gmail.com',
    description='The library provides a lightweight API using which you can in a minute '
                'add a pattern processing function "stringify(pattern: str) -> str" to any class.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/aduard.kononov/strify',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
