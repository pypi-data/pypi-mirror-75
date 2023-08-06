import setuptools

with open('ReadMe.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ChemistryTool',
    version='0.0.1',
    author='Besufikad M. Tilahun',
    author_email='besumicheal@gmail.com',
    description='A module that express chemistry phenomenas interms of algoritihms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Besufikad17/ChemistryTool/Python',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0'
)





