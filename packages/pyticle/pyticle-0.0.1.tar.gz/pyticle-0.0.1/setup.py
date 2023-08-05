import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setuptools.setup(
    name='pyticle',
    version='0.0.1',
    author='Moein Owhadi Kareshk',
    author_email='moein.owhadi@gmail.com',
    description='A Python Library for Particle Swarm Intelligence',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/owhadi/pyticle',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
