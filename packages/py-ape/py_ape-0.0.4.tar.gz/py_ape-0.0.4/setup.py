import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_ape",
    version="0.0.4",
    author="VietPQ - ToiNV",
    author_email="viet20304@gmail.com",
    description="A small package for handling matching data based on BigGorilla package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vietpq/py_ape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'pandas==0.25.1',
      'numpy==1.16.2',
      'scikit-learn==0.19.1',
      'flexmatcher',
      'py_stringsimjoin',
      'py_stringmatching',
      'py_entitymatching',
      'tqdm',
      'beautifulsoup4'
    ],
    python_requires='>=2.7'
)