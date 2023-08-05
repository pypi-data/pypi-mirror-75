import setuptools

# Use the readme.md as the LongDescription parameter for setuptools
with open('readme.md', 'r') as file:
    ld = file.read()

setuptools.setup(
    name='woodchuck',
    version='1.0.0',
    author='Ashwin Mahadevan',
    description='A lightweight, opinionated Python logging package.',
    long_description=ld,
    long_description_content_type='text/markdown',
    url='https://github.com/ShwinHS/woodchuck.git',
    packages=setuptools.find_packages(),
    python_requires='>=3.8'  # This can likely be much, much lower.
)
