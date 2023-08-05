import setuptools

setuptools.setup(
    name="p6",
    version="0.1.5",
    license='MIT',
    author="posix1",
    author_email="posix.lee@gmail.com",
    description="module by posix",
    long_description=open('README.md').read(),
    url="http://p6.is",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)