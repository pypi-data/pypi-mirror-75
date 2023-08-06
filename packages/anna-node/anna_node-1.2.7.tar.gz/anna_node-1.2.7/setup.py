import setuptools

with open('README.md', 'r') as f:
    description = f.read()

setuptools.setup(
    name='anna_node',
    version='1.2.7',
    author='Patrik Pihlstrom',
    author_email='patrik.pihlstrom@gmail.com',
    url='https://github.com/patrikpihlstrom/anna',
    description='simulated & automated end-to-end website testing software',
    long_description=description,
    long_description_content_type='text/markdown',
    packages=['anna'],
    install_requires=[
        'anna_lib',
        'anna_client'
    ]
)
