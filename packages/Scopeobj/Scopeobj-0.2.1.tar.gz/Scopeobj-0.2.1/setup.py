import setuptools

with open("README.txt") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Scopeobj",
    version="0.2.1",
    author="Frank Lin",
    author_email="W_126mail@126.com",
    description="Scope object in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usr8820/PyScope/",
    py_modules=['scopeobj'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0'
)