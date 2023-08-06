import setuptools

with open("README.md", 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name='quotool',
    version='0.0.4',
    author='taner',
    author_email='taner@example.com',
    description='quotool',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/Olaful/',
    packages=['quotool'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
