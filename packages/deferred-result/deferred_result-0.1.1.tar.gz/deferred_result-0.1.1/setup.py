from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="deferred_result",
    version="0.1.1",
    author="Maciej Nowak",
    description="Simple DeferredResult",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Novakov/py-deferred-result",
    packages=['deferred_result'],
    package_data={
        'deferred_result': ['py.typed']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities"
    ],
    python_requires='>=3.7',
    include_package_data=True
)