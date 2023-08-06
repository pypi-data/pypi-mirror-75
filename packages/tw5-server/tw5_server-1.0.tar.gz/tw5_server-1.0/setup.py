import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='tw5_server',
    version='1.0',
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='tiddly wiki server',
    install_requires=['Flask', 'GitPython', 'p_config'],
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)
